# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    #secondary_uom_id = fields.Float(related='product_tmpl_id.secondary_uom_id',string='Secondary (UOM)',readonly=True, store=True)
    secondary_uom = fields.Char(string='UOM', compute='_get_secondary_qty', store=False, readonly=True)
    secondary_qty = fields.Float(string='Secondary Qty', compute='_get_secondary_qty', store=True, readonly=True)

    @api.depends('product_uom_qty')
    def _get_secondary_qty(self):
        """
        Compute the total Quantity Weight of the SO Line.
        """
        for line in self:
            line.secondary_qty = line.product_uom_qty * line.product_id.product_tmpl_id.secondary_unit_qty
            line.secondary_uom = line.product_id.product_tmpl_id.secondary_uom_id.name