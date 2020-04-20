# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    tot_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=True, readonly=True)
    
    @api.depends('order_line','order_line.product_uom_qty')
    def _quantity_all(self):
        """
        Compute the total Quantity and Weight of the SO.
        """
        tot_qty = 0.0
        for order in self:
            for line in order.order_line:
                tot_qty += line.product_uom_qty
            order.tot_qty = tot_qty
            
            
