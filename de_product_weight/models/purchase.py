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
    weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
    price_weight = fields.Float('Weight Price', required=True, digits=dp.get_precision('Weight Price'), default=1.0)
    price_weight_subtotal = fields.Float(compute='_compute_subtotal', string='Subtotal', readonly=True, store=True)
    
    @api.onchange('product_qty')
    def onchange_product_qty(self):
        #super(PurchaseOrderLine, self).onchange_product_id()
        self.total_weight = self.product_id.weight * self.product_qty
        
    @api.depends('weight', 'price_weight')
    def _compute_subtotal(self):
        """
        Compute the amounts of the PO line.
        """
        for line in self:
            line.update({
                'price_weight_subtotal': (line.total_weight * line.price_weight),
                'price_unit': (line.total_weight * line.price_weight),
            })