# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    tot_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=True, readonly=True)
    
    @api.depends('order_line.product_qty')
    def _quantity_all(self):
        """
        Compute the total Quantity.
        """
        tot_qty = 0.0
        for mv in self:
            for line in mv.order_line:
                tot_qty += line.product_qty
            mv.tot_qty = tot_qty