# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    is_sale_weight = fields.Boolean(related='partner_id.is_sale_weight',string='Enable Weight Pricing',readonly=True)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    #def _get_default_price_weight(self):
        #wp = 0
        #if self.sale_line_ids:
            #for sale in self.sale_line_ids:
                #wp = sale.price_weight
        #elif self.purchase_line_id:
            #wp = self.purchase_line.id.price_weight
        #else:
            #wp = 1.0
                
        #return wp
    
    #def _calculate_weight(self):
        #tw = 0
        #if self.move_id.is_sale_weight:
            #if self.sale_line_ids:
                #for sale in self.sale_line_ids:
                    #tw += self.quantity * (sale.total_weight/sale.product_uom_qty)
            #elif self.purchase_line_id:
                #tw = self.quantity * (self.purchase_line.id.total_weight/self.purchase_line_id.product_uom_qty)
            #else:
                #tw = self.weight * self.quantity
                
            #self.total_weight = tw
            #return tw
    
   
                
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=False, store=True)
    #total_weight = fields.Float('Total Weight', store=True, help="Weight of the product in order line")
    total_weight = fields.Float(string='Quantity',default=1.0, digits='Product Unit of Measure',)
    #price_weight = fields.Float('Weight Price', store=True,default='1.0')
    price_weight = fields.Float(string='Unit Price', digits='Product Price')
    
    
    
    
    def write(self, vals):
        # OVERRIDE
        def field_will_change(line, field_name):
            if field_name not in vals:
                return False
            field = line._fields[field_name]
            if field.type == 'many2one':
                return line[field_name].id != vals[field_name]
            if field.type in ('one2many', 'many2many'):
                current_ids = set(line[field_name].ids)
                after_write_ids = set(r['id'] for r in line.resolve_2many_commands(field_name, vals[field_name], fields=['id']))
                return current_ids != after_write_ids
            if field.type == 'monetary' and line[field.currency_field]:
                return not line[field.currency_field].is_zero(line[field_name] - vals[field_name])
            return line[field_name] != vals[field_name]

        ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
        BUSINESS_FIELDS = ('price_unit', 'quantity', 'discount', 'tax_ids','total_weight','price_weight')
        PROTECTED_FIELDS_TAX_LOCK_DATE = ['debit', 'credit', 'tax_line_id', 'tax_ids', 'tag_ids']
        PROTECTED_FIELDS_LOCK_DATE = PROTECTED_FIELDS_TAX_LOCK_DATE + ['account_id', 'journal_id', 'amount_currency', 'currency_id', 'partner_id']
        PROTECTED_FIELDS_RECONCILIATION = ('account_id', 'date', 'debit', 'credit', 'amount_currency', 'currency_id')

        account_to_write = self.env['account.account'].browse(vals['account_id']) if 'account_id' in vals else None

        # Check writing a deprecated account.
        if account_to_write and account_to_write.deprecated:
            raise UserError(_('You cannot use a deprecated account.'))

        # when making a reconciliation on an existing liquidity journal item, mark the payment as reconciled
        for line in self:
            if line.parent_state == 'posted':
                if line.move_id.restrict_mode_hash_table and set(vals).intersection(INTEGRITY_HASH_LINE_FIELDS):
                    raise UserError(_("You cannot edit the following fields due to restrict mode being activated on the journal: %s.") % ', '.join(INTEGRITY_HASH_LINE_FIELDS))
                if any(key in vals for key in ('tax_ids', 'tax_line_ids')):
                    raise UserError(_('You cannot modify the taxes related to a posted journal item, you should reset the journal entry to draft to do so.'))
            if 'statement_line_id' in vals and line.payment_id:
                # In case of an internal transfer, there are 2 liquidity move lines to match with a bank statement
                if all(line.statement_id for line in line.payment_id.move_line_ids.filtered(
                        lambda r: r.id != line.id and r.account_id.internal_type == 'liquidity')):
                    line.payment_id.state = 'reconciled'

            # Check the lock date.
            if any(field_will_change(line, field_name) for field_name in PROTECTED_FIELDS_LOCK_DATE):
                line.move_id._check_fiscalyear_lock_date()

            # Check the tax lock date.
            if any(field_will_change(line, field_name) for field_name in PROTECTED_FIELDS_TAX_LOCK_DATE):
                line._check_tax_lock_date()

            # Check the reconciliation.
            if any(field_will_change(line, field_name) for field_name in PROTECTED_FIELDS_RECONCILIATION):
                line._check_reconciliation()

            # Check switching receivable / payable accounts.
            if account_to_write:
                account_type = line.account_id.user_type_id.type
                if line.move_id.is_sale_document(include_receipts=True):
                    if (account_type == 'receivable' and account_to_write.user_type_id.type != account_type) \
                            or (account_type != 'receivable' and account_to_write.user_type_id.type == 'receivable'):
                        raise UserError(_("You can only set an account having the receivable type on payment terms lines for customer invoice."))
                if line.move_id.is_purchase_document(include_receipts=True):
                    if (account_type == 'payable' and account_to_write.user_type_id.type != account_type) \
                            or (account_type != 'payable' and account_to_write.user_type_id.type == 'payable'):
                        raise UserError(_("You can only set an account having the payable type on payment terms lines for vendor bill."))

        result = super(AccountMoveLine, self).write(vals)

        for line in self:
            if not line.move_id.is_invoice(include_receipts=True):
                continue

            # Ensure consistency between accounting & business fields.
            # As we can't express such synchronization as computed fields without cycling, we need to do it both
            # in onchange and in create/write. So, if something changed in accounting [resp. business] fields,
            # business [resp. accounting] fields are recomputed.
            if any(field in vals for field in ACCOUNTING_FIELDS):
                price_subtotal = line.currency_id and line.amount_currency or line.debit - line.credit
                to_write = line._get_fields_onchange_balance(
                    balance=price_subtotal,
                )
                to_write.update(line._get_price_total_and_subtotal(
                    price_unit=to_write.get('price_unit', line.price_unit),
                    quantity=to_write.get('quantity', line.quantity),
                    discount=to_write.get('discount', line.discount),
                    total_weight=to_write.get('total_weight', line.total_weight),
                    price_weight=to_write.get('price_weight', line.price_weight),
                ))
                super(AccountMoveLine, line).write(to_write)
            elif any(field in vals for field in BUSINESS_FIELDS):
                to_write = self._get_price_total_and_subtotal()
                to_write.update(line._get_fields_onchange_subtotal(
                    price_subtotal=to_write['price_subtotal'],
                ))
                super(AccountMoveLine, line).write(to_write)

        # Check total_debit == total_credit in the related moves.
        if self._context.get('check_move_validity', True):
            self.mapped('move_id')._check_balanced()

        return result
    
    def _get_price_total_and_subtotal(self, price_unit=None, quantity=None, discount=None, currency=None, product=None, partner=None, taxes=None, move_type=None,total_weight=None,price_weight=None):
        self.ensure_one()
        return self._get_price_total_and_subtotal_model(
            price_unit=price_unit or self.price_unit,
            quantity=quantity or self.quantity,
            discount=discount or self.discount,
            currency=currency or self.currency_id,
            product=product or self.product_id,
            partner=partner or self.partner_id,
            taxes=taxes or self.tax_ids,
            move_type=move_type or self.move_id.type,
            #total_weight=total_weight or self.total_weight,
            #price_weight=price_weight or self.price_weight,
        )
    
    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'.
        price_unit_wo_discount = price_unit * (1 - (discount / 100.0))
        subtotal = quantity * price_unit_wo_discount

        # Compute 'price_total'.
        if taxes:
            taxes_res = taxes._origin.compute_all(price_unit_wo_discount,
                quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        return res
    
    #def write(self,vals):
        #res = super(AccountInvoiceLine,self).write(vals)
        
        #for line in self:
            #to_write = line._get_fields_onchange_balance(balance=line.price_subtotal,)
            #to_write.update(line._get_price_total_and_subtotal(
                #price_unit=to_write.get('price_unit', (line.total_weight * line.price_weight) / line.quantity),
                #quantity=to_write.get('quantity', line.quantity),
                #discount=to_write.get('discount', line.discount),
            #))
            #res = super(AccountInvoiceLine,self).write(to_write)
        #super(AccountMoveLine, line).write(to_write)
        #return res
    
    
    #@api.onchange('quantity','price_unit','tmp_price_weight','tmp_total_weight')
    #def _onchange_price_weight(self):
        #pu = 0
        #for line in self:
            #if line.move_id.is_sale_weight and line.quantity > 0:
                #pu = (line.tmp_total_weight * line.tmp_price_weight) / line.quantity
                #line.price_unit = pu
                #self.env.context.update({'price_unit': pu})
                #line.update({
                    #'price_unit': pu
                #}) 
    
    
    