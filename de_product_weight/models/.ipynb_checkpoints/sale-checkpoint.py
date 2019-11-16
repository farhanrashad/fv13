# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	
	weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
	total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
	
	#@api.onchange('product_id', 'product_uom_qty')
	#def product_id_change(self):
		#res = super(SaleOrderLine, self).product_id_change()
		#self.total_weight = self.weight * self.product_uom_qty
		#return res
	
	@api.onchange('product_id')
	def onchange_product_id(self):
		res = super(SaleOrderLine, self).product_id_change()
		for rec in self:
			rec.total_weight = rec.weight * rec.product_uom_qty
		return res

	@api.onchange('product_uom_qty', 'product_uom')
	def _onchange_quantity(self):
		res = super(SaleOrderLine, self).product_id_change()
		for rec in self:
			rec.total_weight = rec.weight * rec.product_uom_qty
		return res

	#api.onchange('product_uom_qty','weight','total_weight')
	#def product_uom_qty_change(self):
		#self.total_weight = self.weight * self.product_uom_qty
        
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    sum_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=True, readonly=True)
    sum_weight = fields.Float(string='Total Weight', compute='_quantity_all', store=True, readonly=True)
    
    @api.depends('order_line.product_uom_qty','order_line.total_weight')
    def _quantity_all(self):
        """
        Compute the total Quantity and Weight of the SO.
        """
        sum_qty = sum_weight = 0.0
        for order in self:
            for line in order.order_line:
                sum_qty += line.product_uom_qty
                sum_weight += (line.weight * line.product_uom_qty)
            order.sum_qty = sum_qty
            order.sum_weight = sum_weight