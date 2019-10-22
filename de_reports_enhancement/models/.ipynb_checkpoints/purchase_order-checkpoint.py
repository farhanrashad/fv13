# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    sum_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=True, readonly=True)
    sum_weight = fields.Float(string='Total Weight', compute='_quantity_all', store=True, readonly=True)
    
    @api.depends('order_line.product_uom_qty')
    def _quantity_all(self):
        """
        Compute the total Quantity and Weight of the SO.
        """
        sum_qty = sum_weight = 0.0
        for order in self:
            for line in order.order_line:
                sum_qty += line.product_uom_qty
                sum_weight += (line.product_weight * line.product_uom_qty)
            order.sum_qty = sum_qty
            order.sum_weight = sum_weight
            
    @api.depends('order_line.product_weight','order_line.product_uom_qty')
    def _weight_all(self):
        """
        Compute the total Quantity and Weight of the SO.
        """
        sum_qty = sum_weight = 0.0
        for order in self:
            for line in order.order_line:
                sum_qty += line.product_uom_qty
                sum_weight += line.product_weight
            order.sum_qty = sum_qty
            order.weight = sum_weight
            
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    product_weight = fields.Float(related='product_id.weight',string='Weight',readonly=True, store=True)
    total_weight = fields.Float(string='Total Weight', compute='_get_total_weight', store=True, readonly=True)

    @api.depends('product_weight','product_uom_qty')
    def _get_total_weight(self):
        """
        Compute the total Quantity Weight of the SO Line.
        """
        for line in self:
            line.total_weight = line.product_weight * line.product_uom_qty