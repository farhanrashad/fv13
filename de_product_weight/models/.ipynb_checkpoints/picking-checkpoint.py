# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp
        
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
            
    def action_confirm(self):
        res = super(StockPicking,self).action_confirm()
        for move in self.move_lines:
            #if move.location_id.usage == 'internal':
                #move.product_id.product_tmpl_id.weight_available += move.total_weight
            #elif move.location_dest_id.usage == 'internal':
                #move.product_id.product_tmpl_id.weight_available -= move.total_weight
                
            #if move.product_id.product_tmpl_id.tracking == 'none':
            quant_from = self.env['stock.quant'].search([('product_id', '=', move.product_id.id),('location_id', '=', move.location_id.id)])
            quant_to = self.env['stock.quant'].search([('product_id', '=', move.product_id.id),('location_id', '=', move.location_dest_id.id)])
                
            #self.env['stock.quant'].sudo().update({
            #    'product_weight': 11,
            #})
            quant = self.env['stock.quant']
            #quant.product_weight == 12
        
        return res