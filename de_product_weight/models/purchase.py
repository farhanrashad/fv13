# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    #def _default_total_weight(self):
        #return self.product_id.weight * self.product_qty
        
    #weight = fields.Float('Weight/Kg', digits=dp.get_precision('Stock Weight'), default=_default_product_weight, help="Weight of the product, packaging not included. The unit of measure can be changed in the general settings")
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line", default=1.0)
    price_weight = fields.Float('Weight Price', required=True, digits=dp.get_precision('Weight Price'), default=1.0)
    price_weight_subtotal = fields.Float(string='Subtotal', readonly=True, store=True)
    
    @api.onchange('product_qty')
    def onchange_product_qty(self):
        #super(PurchaseOrderLine, self).onchange_product_id()
        self.total_weight = self.product_id.weight * self.product_qty
        
    #@api.depends('total_weight', 'price_weight')
    @api.onchange('product_qty','total_weight','price_weight')
    def _compute_subtotal(self):
        """
        Compute the amounts of the PO line.
        """
        for line in self:
            if line.price_weight > 0 and line.product_qty > 0  and line.total_weight > 0:
                #line.price_weight_subtotal = (line.total_weight * line.price_weight)
                line.price_unit = (line.total_weight * line.price_weight) / line.product_qty
                
                #line.update({
                 #   'price_weight_subtotal': (line.total_weight * line.price_weight),
                  #  'price_unit': line.product_qty / (line.total_weight * line.price_weight),
                #})
            
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    sum_qty = fields.Float(string='Total Quantity', compute='_sum_quantity', store=True, readonly=True)
    sum_weight = fields.Float(string='Total Weight', compute='_sum_quantity', store=True, readonly=True)
    
    @api.depends('order_line.product_uom_qty','order_line.total_weight')
    def _sum_quantity(self):
        """
        Compute the sum of Quantity and Weight of the order lines.
        """
        
        for order in self:
            sum_qty = sum_weight = 0.0
            for line in order.order_line:
                sum_qty += line.product_uom_qty
                sum_weight += line.total_weight
            order.sum_qty = sum_qty
            order.sum_weight = sum_weight