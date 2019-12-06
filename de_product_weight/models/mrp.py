# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    #weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    #total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
    production_weight = fields.Float('Weight to produce', compute='_get_production_weight', readonly=True, store=True, digits=dp.get_precision('Stock Weight'), help="Weight to be produce")
    
    @api.depends('product_id','product_qty')
    def _get_production_weight(self):
        for order in self:
            order.production_weight = order.product_id.weight * order.product_qty
    #@api.onchange('product_qty')
    #def onchange_product_uom_qty(self):
        #self.total_weight = self.product_id.weight * self.product_qty
		
	#def button_mark_done(self):
		#super(MrpProduction, self).button_mark_done()

    
        
class MRPProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'
    
    produced_weight = fields.Float('Weight Produced', digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    @api.onchange('qty_producing')
    def _compute_produced_weight(self):
        """
        Compute the weight on change in quantity
        """
        self.produced_weight = self.qty_producing * self.product_id.weight
        
            
    def do_produce(self):
        """ Save the current wizard and go back to the MO. """
        res = super(MRPProductProduce, self).do_produce()
        self._product_weight_assignment()
        #for mv in self.move_raw_ids:
            #mv.total_weight = 10
        #for line in self.raw_workorder_line_ids:
            #for mv in line.move_id.move_line_ids:
                #mv.total_weight = line.produced_weight
            #for mv in line.move_id.move_line_ids:
                #mv.total_weight = line.produced_weight
        return res
    
    def continue_production(self):
        res = super(MRPProductProduce, self).continue_production()
        self._product_weight_assignment()
        #for line in self.raw_workorder_line_ids:
        
                #line.toal_weight = 111
        
        
                
        #for line in self.production_id.move_raw_ids:
            #production = self.env['mrp.product.produce.line'].search([('move_id', '=', line.id)],limit=1)
            #for mv in line.move_line_ids:
            #    mv.total_weight = production.produced_weight
            #move_lines = self.env['stock.move.line'].search([('move_id', '=', line.move_id.id)])
            #for mv in move_lines:
                #mv.write({
                #'total_weight': 10,
                #})
        return res
    
    def _product_weight_assignment(self):
        #finish weight assignment
        for mv in self.production_id.move_finished_ids:
            for line in mv.move_line_ids:
                if line.lot_id == self.finished_lot_id:
                    line.write({
                        'total_weight': self.produced_weight,
                    })
        
        #raw material weight assignment
        for raws in self.production_id.move_raw_ids:
            for rline in raws.move_line_ids:
                for lot in rline.lot_produced_ids:
                    if lot == self.finished_lot_id:
                        if not(rline.product_id.product_tmpl_id.uom_id.category_id.measure_type == 'weight'):
                            rline.write({
                                'total_weight': self.produced_weight * (rline.move_id.bom_line_id.product_qty/rline.move_id.bom_line_id.bom_id.product_qty)
                            })
                        else:
                            rline.write({
                                'qty_done': self.produced_weight * (rline.move_id.bom_line_id.product_qty/rline.move_id.bom_line_id.bom_id.product_qty)
                            })
                        
    
            
class MRPProductProduceLine(models.TransientModel):
    _inherit = 'mrp.product.produce.line'
    
    produced_weight = fields.Float('Weight Produced', compute='_calculate_produced_weight', store=True, digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    @api.depends('raw_product_produce_id.produced_weight')
    def _calculate_produced_weight(self):
        for rs in self:
            if rs.product_id.product_tmpl_id.is_weight_uom:
                rs.produced_weight = rs.raw_product_produce_id.produced_weight * (rs.move_id.bom_line_id.product_qty/rs.move_id.bom_line_id.bom_id.product_qty)
            else:
                rs.produced_weight = 0
            
    @api.onchange('raw_product_produce_id.produced_weight')
    def _change_produced_qty(self):
        """
        Compute the weight on change in quantity
        """
        for rs in self:
            if not(rs.product_id.product_tmpl_id.is_weight_uom):
                rs.qty_done = rs.raw_product_produce_id.produced_weight * (rs.move_id.bom_line_id.product_qty/rs.move_id.bom_line_id.bom_id.product_qty)
           
    