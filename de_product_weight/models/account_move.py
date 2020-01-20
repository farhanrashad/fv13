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

class AccountInvoiceLine(models.Model):
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
    total_weight = fields.Float('Total Weight', store=True, help="Weight of the product in order line")
    price_weight = fields.Float('Weight Price', store=True,)
    tmp_total_weight = fields.Float('tmp Total Weight',compute='_get_tmp_weight')
    tmp_price_weight = fields.Float('tmp Weight Price',compute='_get_tmp_weight')
    
    def _get_tmp_weight(self):
        self.tmp_price_weight = self.price_weight
        self.tmp_total_weight = self.total_weight
    
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
    
    @api.onchange('quantity','price_unit','tmp_price_weight','tmp_total_weight')
    def _onchange_price_weight(self):
        pu = 0
        for line in self:
            if line.move_id.is_sale_weight and line.quantity > 0:
                pu = (line.tmp_total_weight * line.tmp_price_weight) / line.quantity
                line.update({
                    'price_unit': pu
                }) 
    
    #def _get_computed_price_unit(self):
        #res = super(AccountInvoiceLine,self)._get_computed_price_unit()
        #if self.move_id.is_sale_weight:
            #price_unit = (self.total_weight * self.price_weight) / self.quantity
        #return res
        
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
            total_weight=total_weight or self.total_weight,
            price_weight=price_weight or self.price_weight,
        )
    
    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type,total_weight=None,price_weight=None):
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
        subtotal = price_unit_wo_discount = new_price = 0
        if self.move_id.is_sale_weight:
            if self.quantity > 0:
                new_price = (self.total_weight * self.price_weight) / self.quantity
                #price_unit_wo_discount = new_price * (1 - (discount / 100.0))
                #res['price_unit'] = new_price
                price_unit = new_price
        #else:
            #price_unit_wo_discount = price_unit * (1 - (discount / 100.0))
            #subtotal = quantity * price_unit_wo_discount
        
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
    
    
    #@api.onchange('product_id','quantity')
    #def _onchange_quantity(self):
        #self._calculate_weight()
    
    #@api.onchange('weight')
    #def _onchange_weight(self):
        #self.total_weight = self.quantity * self.weight
       
   
                
    