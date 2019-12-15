# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
	_inherit = 'stock.move'
	
	total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), compute='_get_total_weight', store=True, readonly=True)
	
	@api.depends('quantity_done')
	def _get_total_weight(self):
		sum_weight = 0.0
		for mv in self:
			for line in mv.move_line_ids:
				sum_weight += line.total_weight
			mv.total_weight = sum_weight
	
	#@api.depends('product_id','quantity_done')
	#def _get_total_weight(self):
		#for line in self.move_line_ids:
			#if self.product_id == line.product_id:
				#self.total_weight = line.total_weight
			
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
    
    #def _quantity_done_set(self):
    #def _action_cancel(self):
    #def _action_done(self, cancel_backorder=False):
    #def _set_quantity_done(self, qty):
        
    def write(self, vals):
        res = super(StockMoveLine, self).write(vals)
        for rs in self:
            if rs.product_id.product_tmpl_id.is_weight_uom:
                if rs.location_id.usage == 'internal':
                    rs.product_id.product_tmpl_id.weight_available -= rs.total_weight
                    if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        rs.lot_id.product_weight -= rs.total_weight
                elif rs.location_dest_id == 'internal':
                    rs.product_id.product_tmpl_id.weight_available += rs.total_weight
                    if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        rs.lot_id.product_weight += rs.total_weight
                    
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