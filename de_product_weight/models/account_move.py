# -*- coding: utf-8 -*-
from odoo import models,fields,api,_

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    is_sale_weight = fields.Boolean(related='partner_id.is_sale_weight',string='Enable Weight Pricing',readonly=True)
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=True, store=True)
    total_weight = fields.Float(string='Total Weight',default=1.0)
    price_weight = fields.Float(string='Price Weight', digits='Product Price')
    
    price_qty_weight = fields.Float(string='Price Qty/Weight', store=False, digits='Product Price',compute='_compute_price_weight')
    
    def _compute_price_weight(self):
        for line in self:
            if line.quantity > 0:
                line.price_qty_weight = (line.total_weight * line.price_weight) / line.quantity
                
    @api.onchange('quantity','weight')
    def _onchange_weight(self):
        for line in self:
            line.total_weight = line.weight * line.quantity
            
    @api.model_create_multi
    def create(self, vals_list):
        self.update({
            'total_weight': self.quantity * self.weight
        })
        res = super(AccountMoveLine,self).create(vals_list)
        return res
            
