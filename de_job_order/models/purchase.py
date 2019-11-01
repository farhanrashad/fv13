# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    job_order_id = fields.Many2one('Job.order', string='Job Order Reference', required=False, ondelete='cascade', index=True, copy=False, readonly=True)
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    weight = fields.Float('Weight/Kg', digits=dp.get_precision('Stock Weight'), help="Weight of the product, packaging not included. The unit of measure can be changed in the general settings")
    price_weight = fields.Float('Weight Price', required=True, digits=dp.get_precision('Weight Price'), default=1.0)
    price_weight_subtotal = fields.Float(compute='_compute_subtotal', string='Subtotal', readonly=True, store=True)
    
    @api.depends('weight', 'price_weight')
    def _compute_subtotal(self):
        """
        Compute the amounts of the PO line.
        """
        for line in self:
            line.update({
                'price_weight_subtotal': (line.weight * line.price_weight),
                'price_unit': (line.weight * line.price_weight),
            })
            #line.weight = line.product_id.weight
                
        