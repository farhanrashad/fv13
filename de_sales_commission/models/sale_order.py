# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one('res.partner', string='Agent', required=False, readonly=True,
                                         states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                         help="To address a contact in care of someone else")
    
    commission_amount = fields.Monetary(string='Commission Amount', store=True, readonly=True, compute='_amount_all')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.agent_id = self.partner_id.agent_id
        #self.commission_percentage = self.partner_id.commission_percentage

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """Compute the C/O Commission amounts of the SO"""
        res = super(SaleOrder, self)._amount_all()
        for order in self:
            order.update({
                'commission_amount': order.amount_untaxed
            })
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    commission_percentage = fields.Float(string='Comm. %', readonly=True,
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        #super(SaleOrderLine, self).onchange_product_id()
        self.commission_percentage = self.order_id.partner_id.commission_percentage