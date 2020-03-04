# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderApproval(models.Model):
    _inherit = 'sale.order'

    def submit_for_approval(self):
        for rec in self:
            rec.state = 'waiting_for_approval'

    def approve_sale_order(self):
        for rec in self:
            rec.state = 'sale'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('waiting_for_approval', 'Waiting For Approval'),
        ('sale', 'Sale Order'),
    ], readonly=True, string='Status')
# class de_approval_state(models.Model):
#     _name = 'de_approval_state.de_approval_state'
#     _description = 'de_approval_state.de_approval_state'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
