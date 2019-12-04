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