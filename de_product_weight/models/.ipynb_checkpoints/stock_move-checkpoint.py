# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), compute='_calculate_total_weight', readonly=True)
            
    @api.depends('move_line_ids','move_line_nosuggest_ids','product_id')
    def _calculate_total_weight(self):
        for line in self:
            sum_weight = sum_weight1 = 0
            for move_line in line.move_line_ids:
                if not move_line.total_weight:
                    sum_weight += move_line.qty_done * move_line.weight
                else:
                    sum_weight += move_line.total_weight
            line.total_weight = sum_weight
			
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), readonly=False, help="Weight of the product in order line")
    
    @api.depends('product_id','lot_id','qty_done', 'weight')
    def _calculate_total_weight(self):
        for line in self:
            if line.total_weight == 0 or not line.total_weight:
                line.total_weight = line.qty_done * line.weight
            
    @api.onchange('product_id','lot_id')
    def onchange_product(self):
        if self.lot_id:
            self.qty_done = self.lot_id.product_qty
                
        
    def write(self, vals):
        #Raw Material Assignment
        res = super(StockMoveLine, self).write(vals)
        #self.product_id.product_tmpl_id.weight_available = self.product_id.product_tmpl_id.weight_available + self.total_weight
        for rs in self.filtered(lambda x: x.move_id.state in ('done')):
            if rs.product_id.product_tmpl_id.is_weight_uom:
                if rs.location_dest_id.usage == 'internal':
                    rs.product_id.weight_available += rs.total_weight
                    if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        rs.lot_id.product_weight += rs.total_weight
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_dest_id.id),('lot_id', '=', rs.lot_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.lot_id.product_weight
                        })
                    else:
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_dest_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.total_weight
                        }) 
                elif rs.location_id.usage == 'internal':
                    rs.product_id.weight_available -= rs.total_weight
                    if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        rs.lot_id.product_weight -= rs.total_weight
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_id.id),('lot_id', '=', rs.lot_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.lot_id.product_weight
                        })
                    else:
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.total_weight
                        }) 
                    
                #if rs.location_id.usage == 'internal':
                    #rs.product_id.product_tmpl_id.weight_available = rs.total_weight
                    #if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        #rs.lot_id.product_weight -= rs.total_weight
                #elif rs.location_dest_id == 'internal':
                    #rs.product_id.product_tmpl_id.weight_available = rs.product_id.product_tmpl_id.weight_available + rs.total_weight
                    #if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        #rs.lot_id.product_weight += rs.total_weight
                    
        return res