# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    real_quantity = fields.Float('Real Quantity',compute='_compute_real_quantity')
    
    #@api.depends('product_id','qty_done')
    def _compute_real_quantity(self):
        qty = 0
        for line in self:
            if line.location_dest_id.usage != 'internal' and line.location_id.usage == 'internal':
                qty = line.qty_done * -1
            elif line.location_dest_id.usage == 'internal' and line.location_id.usage != 'internal':
                qty = line.qty_done
            line.update({
                'real_quantity': qty,
            })