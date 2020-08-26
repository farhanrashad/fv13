# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from collections import defaultdict
from odoo.exceptions import UserError
from datetime import date
from datetime import datetime , timedelta




class PurchaseOrderMultiple(models.Model):
    _name = 'purchase.order.multiple'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Multiple Purchase Order'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.multiple') or 'New'
        result = super(PurchaseOrderMultiple, self).create(vals)
        return result

    

    

    def action_generate_po(self):
        for line in self.sheet_ids:
            if line.product_quantity > 0:
                supplier_line = {
                    'product_id': line.product_id.id,
                    'name': 'Product',
                    'product_qty': line.product_quantity,
                    'price_unit': line.product_id.list_price,
                    'order_id': self.id,
                    'date_planned': fields.Date.today(),
                    'product_uom': line.product_id.uom_id.id,
                }
                b_prod = self.env['product.product'].search([('id', '=', line.product_id.id)])
                b_prod_line = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', b_prod.id)], limit=1)
                print(b_prod_line.name.name)
                self.env['purchase.order'].create({
                    'partner_id': line.vendor_id.id,
#                     'jo_sheet_reference': self.name,
                    # 'sale_order_ref': rec.job_order_id.sale_order_id.name,
                    'date_order': fields.Date.today(),
                    'order_line': [(0, 0, supplier_line)],
                })
                self.write({
                    'po_created': True
                })


    name = fields.Char(
        'Reference', copy=False, readonly=True, default=lambda x: _('New'))
    date = fields.Date(string='Date', store=True, default=datetime.today())
    po_created = fields.Boolean(string='PO Created')
    space = fields.Char(default=" ", readonly=True)
    sheet_ids = fields.One2many(comodel_name='purchase.order.multiple.line', inverse_name='sheet_id')


class JobOrderSheetLine(models.Model):
    _name = 'purchase.order.multiple.line'
    _description = 'Material Planning'



    sheet_id = fields.Many2one(comodel_name='purchase.order.multiple')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    product_name = fields.Char(string='Product Name', related='product_id.name')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    product_quantity = fields.Float(string='Quantity')
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor', required=True)
