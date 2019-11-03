# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), compute='_get_total_weight', help="Weight of the product in order line")
    
    @api.depends('move_line_ids')
    def _get_total_weight(self):
        for line in self.move_line_ids:
            self.total_weight += line.total_weight
    
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
    
    @api.onchange('product_uom_qty')
    def onchange_product_uom_qty(self):
        self.total_weight = self.product_id.weight * self.product_uom_qty
    
    @api.onchange('qty_done')
    def onchange_product_qty_done(self):
        self.total_weight = self.product_id.weight * self.qty_done
        
        
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    sum_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=True, readonly=True)
    sum_weight = fields.Float(string='Total Weight', compute='_quantity_all', store=True, readonly=True)
    
    @api.depends('move_line_ids.qty_done','move_line_ids.total_weight')
    def _quantity_all(self):
        """
        Compute the total Quantity and Weight of the SO.
        """
        sum_qty = sum_weight = 0.0
        for mv in self:
            for line in mv.move_line_ids:
                sum_qty += line.qty_done
                sum_weight += line.total_weight
            mv.sum_qty = sum_qty
            mv.sum_weight = sum_weight