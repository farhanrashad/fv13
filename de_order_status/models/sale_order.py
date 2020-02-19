# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_status = fields.Char(string='Delivery Status', compute="_compute_delivert_status")
    due_amount = fields.Monetary(string='Due Amount', compute='_compute_payment')

    def _compute_delivert_status(self):
        for so in self:
            moves = so.order_line.mapped('move_ids')
            moves_not_cancel = self.env['stock.move']
            if moves:
                so.delivery_status = 'Draft'
                moves_not_cancel = moves.filtered(lambda x: x.state != 'cancel')
                if all(m.state == 'cancel' for m in moves):
                    so.delivery_status = 'Cancelled'
            if moves_not_cancel:
                if any(m.state not in ('assigned', 'done') for m in moves_not_cancel):
                    so.delivery_status = 'Waiting'
                if all(m.state == 'assigned' for m in moves_not_cancel):
                    so.delivery_status = 'Ready'
                if any(m.state == 'done' for m in moves_not_cancel):
                    so.delivery_status = 'Partially Delivered'
                if all(m.state == 'done' for m in moves_not_cancel):
                    so.delivery_status = 'Fully Delivered'

    def _compute_payment(self):
        payment = 0
        for line in self:
            if len(line.invoice_ids):
                payment = sum(line.invoice_ids.mapped('amount_residual'))
            else:
                payment = line.amount_total
                
            line.update({
                'due_amount': payment,
            })
            #pending_amount = round(inv_amount - amount, 2)
            #if inv_amount  < amount:
                #pending_amount = 0.0
            #so.invoice_paid_details = '( %s / %s )' % (amount, pending_amount)