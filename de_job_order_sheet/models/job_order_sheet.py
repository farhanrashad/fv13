# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from collections import defaultdict
from odoo.exceptions import UserError


class StockRuleExt(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_manufacture(self, procurements):
        productions_values_by_company = defaultdict(list)
        for procurement, rule in procurements:
            bom = self._get_matching_bom(procurement.product_id, procurement.company_id, procurement.values)
            if not bom:
                msg = _(
                    'There is no Bill of Material of type manufacture or kit found for the product %s. Please define a Bill of Material for this product.') % (
                      procurement.product_id.display_name,)
                raise UserError(msg)

            productions_values_by_company[procurement.company_id.id].append(rule._prepare_mo_vals(*procurement, bom))

        for company_id, productions_values in productions_values_by_company.items():
            # create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
            # productions_values['sale_reference'] = productions_values[1]
            productions = self.env['mrp.production'].sudo().with_context(force_company=company_id).create(
                productions_values)
            for prod in productions:
                source = prod.origin
                productions.update({
                    'sale_reference': source
                })
            self.env['stock.move'].sudo().create(productions._get_moves_raw_values())
            productions.action_confirm()

            for production in productions:
                origin_production = production.move_dest_ids and production.move_dest_ids[
                    0].raw_material_production_id or False
                orderpoint = production.orderpoint_id
                if orderpoint:
                    production.message_post_with_view('mail.message_origin_link',
                                                      values={'self': production, 'origin': orderpoint},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
                if origin_production:
                    production.message_post_with_view('mail.message_origin_link',
                                                      values={'self': production, 'origin': origin_production},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        return True


class MrpProductionExt(models.Model):
    _inherit = 'mrp.production'

    sale_reference = fields.Char(string='Sale Reference')


class JobOrderSheet(models.Model):
    _name = 'job.order.sheet'
    _description = 'Job Order Sheet'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('job.order.sheet') or 'New'
        result = super(JobOrderSheet, self).create(vals)
        return result

    def get_sheet_lines(self):
        for rec in self:
            rec.sheet_ids.unlink()
            order_data = self.env['mrp.production'].search(['&', ('sale_reference', '=', rec.sale_order_id.name),
                                                            '|',
                                                            ('product_id', '=like', '[Unfinished]%'),
                                                            ('product_id', '=like', '[Module]%')])
            for order in order_data:
                rec.sheet_ids |= rec.sheet_ids.new({
                    'mo_order_id': order.id,
                    'product_id': order.product_id.id,
                    'product_quantity': order.product_qty,
                })

    def action_approve(self):
        self.state = 'approved'

    def action_completed(self):
        self.state = 'done'

    def action_quantity_update(self):
        for line in self.sheet_ids:
            update_qty = line.in_house_production + line.outsource_production
            order = self.env['mrp.production'].search([('id', '=', line.mo_order_id.id)])
            order.update({
                'product_qty': line.in_house_production
            })

    name = fields.Char(
        'Reference', copy=False, readonly=True, default=lambda x: _('New'))
    date = fields.Date(string='Date', required=True)
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Completed')],
        readonly=True, string='State', default='draft')
    sheet_ids = fields.One2many(comodel_name='job.order.sheet.line', inverse_name='sheet_id')


class JobOrderSheetLine(models.Model):
    _name = 'job.order.sheet.line'
    _description = 'Material Planning'

    def update_product_quantity(self):
        for rec in self:
            self.write({
                'product_quantity': rec.update_quantity,
            })
            order = self.env['mrp.production'].search([('id', '=', rec.mo_order_id.id)])
            order.update({
                'product_qty': rec.update_quantity,
            })

    sheet_id = fields.Many2one(comodel_name='job.order.sheet')
    mo_order_id = fields.Many2one(comodel_name='mrp.production', string='Reference', required=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    product_quantity = fields.Float(string='Quantity')
    in_house_production = fields.Float(string='InHouse Production')
    outsource_production = fields.Float(string='Outsource Production')
