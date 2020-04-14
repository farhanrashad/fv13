# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
  
    production_weight = fields.Float('Weight to produce', compute='_get_production_weight', readonly=True, store=True, digits=dp.get_precision('Stock Weight'), help="Weight to be produce")
    
    @api.depends('product_id','product_qty')
    def _get_production_weight(self):
        for order in self:
            order.production_weight = order.product_id.weight * order.product_qty

    
    
                
class MrpProductionLog(models.Model):
    _name = 'mrp.production.log'
    
    product_id = fields.Many2one('product.product', 'Product Variant',)
    lot_id = fields.Many2one('stock.production.lot','lot')
    move_id = fields.Many2one('stock.move','Move')
    move_line_id = fields.Many2one('stock.move.line','Move Line')
    product_produce_id = fields.Integer('Product Produce')
    product_produce_line_id = fields.Integer('Product Produce Line')
    qty_done = fields.Float(string="quantity")
    consumed_weight = fields.Float('Consumed Weight', store=True, digits=dp.get_precision('Stock Weight'), help="Weight consumed", oldname='total_weight')
    finished_product_id = fields.Many2one('product.product', 'Finish Product',)
    finished_lot_id = fields.Many2one('stock.production.lot','Finish Lot')
    finished_qty_done = fields.Float(string="Finish quantity")
    finished_produced_weight = fields.Float('Produced Weight', store=True, digits=dp.get_precision('Stock Weight'), help="Produced Weight")
    
    
           
    