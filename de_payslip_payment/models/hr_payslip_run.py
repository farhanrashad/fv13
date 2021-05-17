# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HRPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    journal_id = fields.Many2one("account.journal", domain="[('type','in',['bank','cash'])]", )
    payment_method_id = fields.Many2one("account.payment.method", string="Payment Method", domain="[('payment_type','=','outbound')]")
    paid = fields.Boolean(string="Paid", readonly=True)

    
    def generate_payment_batch(self):
        vals = {}
        batch_payment_id = self.env['account.batch.deposit'].create({
            'batch_type': 'outbound',
            'journal_id': self.journal_id.id,
            'payment_method_id': self.payment_method_id.id,
            'date': self.create_date,
            'name': self.name,
        })
        for line in self.slip_ids:
            if line.employee_id.address_home_id.id and line.state !='paid':
                vals = {
                    'payment_type': 'outbound',
                    'partner_type': 'supplier',
                    'partner_id': line.employee_id.address_home_id.id,
                    'amount': line.contract_id.wage,
                    'date': line.date_from,
                    'ref': line.name,
                    'journal_id': self.journal_id.id,
                    'state': 'draft',
                    'payment_method_id': self.payment_method_id.id,
                   'batch_deposit_id': batch_payment_id.id,                    
                }
                line.update({
                    'state': 'paid'
                })
                payment_id = self.env['account.payment'].create(vals)
