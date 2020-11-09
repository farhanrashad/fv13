# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    def action_view_invoice(self):
        res = super(PurchaseOrder, self).action_view_invoice()
        bills = self.env['account.move.line'].search([('ivoice_origin','=', self.name)])
        for bill in bills:            
            bill.write({
               'job_id': self.job_order_id.id,
               'sale_id': self.sale_id.id,
               'purchases_id': self.purchases_id.id, 
            })     
        return res
    

#     name = fields.Char()
#     value = fields.Integer()


class AccountMove(models.Model):
    _inherit = 'account.move'
    

    broke = fields.Char(string='Broke')
    job_id = fields.Many2one('job.order', string="Job Order", store= True)
    sale_id = fields.Many2one('sale.order', string="Job Order", store= True)
    purchases_id = fields.Many2one('purchase.order', string='PO Order', store= True)
