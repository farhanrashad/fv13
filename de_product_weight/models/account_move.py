# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    is_sale_weight = fields.Boolean(related='partner_id.is_sale_weight',string='Enable Weight Pricing',readonly=True)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    #def _get_default_price_weight(self):
        #wp = 0
        #if self.sale_line_ids:
            #for sale in self.sale_line_ids:
                #wp = sale.price_weight
        #elif self.purchase_line_id:
            #wp = self.purchase_line.id.price_weight
        #else:
            #wp = 1.0
                
        #return wp
    
    #def _calculate_weight(self):
        #tw = 0
        #if self.move_id.is_sale_weight:
            #if self.sale_line_ids:
                #for sale in self.sale_line_ids:
                    #tw += self.quantity * (sale.total_weight/sale.product_uom_qty)
            #elif self.purchase_line_id:
                #tw = self.quantity * (self.purchase_line.id.total_weight/self.purchase_line_id.product_uom_qty)
            #else:
                #tw = self.weight * self.quantity
                
            #self.total_weight = tw
            #return tw
                
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=False, store=True)
    total_weight = fields.Float('Total Weight', store=True, digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
    price_weight = fields.Float('Weight Price', store=True, digits=dp.get_precision('Weight Price'), domain="[('parent.is_sale_weight', '=', True)")
    
    
    
    #@api.onchange('product_id','quantity')
    #def _onchange_quantity(self):
        #self._calculate_weight()
    
    #@api.onchange('weight')
    #def _onchange_weight(self):
        #self.total_weight = self.quantity * self.weight
    
    @api.onchange('price_weight')
    def _onchange_price_weight(self):
        for line in self:
            if line.quantity > 0:
                line.price_unit = (line.total_weight * line.price_weight) / line.quantity
                
    