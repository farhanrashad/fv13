# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp



class SalestimateLine(models.Model):
    _name = 'sale.estimate.line'

    @api.onchange('product_id')
    def set_products_auto(self):
        for rec in self:
            rec.price_unit = rec.product_id.lst_price
            rec.name = rec.product_id.name
            rec.product_uom = rec.product_id.uom_id

    product_id = fields.Many2one('product.product', string='Product')
    order_id = fields.Many2one('sale.estimate', string='Reference')
    name = fields.Text(string='Description')
    price_unit = fields.Float('Unit Price',  digits='Product Price', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    # currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    # price_subtotal = fields.Monetary(string='Subtotal', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0 )
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    price_unit_id = fields.Float('Unit Price', digits='Product Price', default=0.0)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', default=1.0)
    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)])
    price_total = fields.Monetary(compute='_compute_amount', string='Total Estimate', readonly=True, store=True)
    product_custom_attribute_value_ids = fields.One2many('product.attribute.custom.value', 'sale_order_line_id',
                                                         string="Custom Values")
    product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Extra Values",
                                                              ondelete='restrict')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id)
            line.update({
                # 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                # 'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
