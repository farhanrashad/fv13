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
    
    produced_weight = fields.Float('Weight to produce', digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    #def do_produce(self):
        #res = super(MRPProductProduce, self).do_produce()
        #production_id = self.env['stock.move.line'].search([('production_id', '=', self.production_id.id),('product_id', '=', self.product_id.id),('lot_id', '=', self.lot_id.id)],limited=1)
        
        #for p in produceproduction_id:
            #p.update({
                #'total_weight': self.produced_weight,
            #})
            #p.total_weight = self.produced_weight
   # @api.onchange('produced_weight')
   # def _onchange_produced_weight(self):
        #for line in self.raw_workorder_line_ids:
            #for bom_line in self.line.production_id.bom_id.bom_line_ids:
                #if bom_line.product_id.id == line.product_id.id:
                    #line.produced_weight = self.produced_weight * (1 / bom_line.product_qty)
            
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
                        rline.write({
                            'total_weight': self.produced_weight * (rline.move_id.bom_line_id.product_qty/rline.move_id.bom_line_id.bom_id.product_qty)
                        })
                        
    
            
class MRPProductProduceLine(models.TransientModel):
    _inherit = 'mrp.product.produce.line'
    
    produced_weight = fields.Float('Weight to produce', compute='_calculate_produced_weight', store=True, digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    @api.depends('raw_product_produce_id.produced_weight')
    def _calculate_produced_weight(self):
        for rs in self:
            rs.produced_weight = rs.raw_product_produce_id.produced_weight * (rs.move_id.bom_line_id.product_qty/rs.move_id.bom_line_id.bom_id.product_qty)
            #rs.move_id.total_weight += rs.produced_weight
            #for mv in rs.move_id.move_line_ids:
                #mv.total_weight = rs.produced_weight
            #for bom_line in rs.raw_product_produce_id.production_id.bom_id.bom_line_ids:
                #if rs.product_id == bom_line.product_id:
                    #rs.produced_weight = rs.raw_product_produce_id.produced_weight * (1/bom_line.product_qty)
    