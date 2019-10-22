# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_weight = fields.Float(related='product_id.weight',string='Weight',readonly=True, store=True)
    total_weight = fields.Float(string='Total Weight', compute='_get_total_weight', store=True, readonly=True)

    @api.depends('product_weight','product_uom_qty')
    def _get_total_weight(self):
        """
        Compute the total Quantity Weight of the SO Line.
        """
        for line in self:
            line.total_weight = line.product_weight * line.product_uom_qty