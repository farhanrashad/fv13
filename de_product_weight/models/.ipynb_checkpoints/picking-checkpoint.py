# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), compute='_get_total_weight', store=False, readonly=True)
    
    @api.depends('move_line_ids')
    def _get_total_weight(self):
        sum_weight = 0.0
        for mv in self:
            for line in mv.move_line_ids:
                sum_weight += line.total_weight
            mv.update({
                'total_weight': sum_weight
            })
    
    
    #@api.depends('product_id','quantity_done')
	#def _get_total_weight(self):
		#for line in self.move_line_ids:
			#if self.product_id == line.product_id:
				#self.total_weight = line.total_weight
			
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
    
    @api.onchange('product_id','lot_id')
    def onchange_product(self):
        if self.product_id.product_tmpl_id.is_weight_uom:
            if self.lot_id:
                self.qty_done = self.lot_id.product_qty
                if self.lot_id.product_weight > 0:
                    self.total_weight = self.lot_id.product_weight 
                else:
                    self.total_weight = (self.product_id.weight * self.lot_id.product_qty)
            else:
                self.total_weight = self.product_id.weight_available
                
            
    @api.onchange('qty_done')
    def onchange_quantity(self):
        if self.product_id.product_tmpl_id.is_weight_uom:
            if self.lot_id and self.lot_id.product_weight > 0:
                self.total_weight = self.qty_done * (self.lot_id.product_weight / self.lot_id.product_qty) or self.qty_done * self.product_id.weight
            elif self.lot_id and self.lot_id.product_weight <= 0:
                self.total_weight = self.qty_done * self.product_id.weight
        
        
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