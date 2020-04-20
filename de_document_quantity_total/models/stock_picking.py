# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp
        
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    tot_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=True, readonly=True, default=0.0)
    
    @api.depends('move_line_ids.qty_done')
    def _quantity_all(self):
        """
        Compute the total Quantity
        """
        tot_qty = 0.0
        for line in self.move_line_ids:
            if line.tot_qty:
                line.tot_qty += line.qty_done
            #mv.tot_qty = tot_qty
