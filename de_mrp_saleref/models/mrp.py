# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Char(string='Ref Sale', compute='_compute_sale_ref')
    
    @api.depends('origin')
    def _compute_sale_ref(self):
        for list in self:
            test = self.env['sale.order'].search([('name','=', list.origin)], limit=1)
            list.sale_id = test.name
        
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
#     def action_confirm(self):
#         res = super(SaleOrder, self).action_confirm()
#         vals = {
#             'sale_id': self.name,
#         }
#         test = self.env['mrp.production'].write(vals)
#         return res
