# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountReportPayment(models.TransientModel):
    _name = "account.report.payment"
    _description = "Account Payment Report"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True,
                                   default=lambda self: self.env['account.journal'].search(
                                       [('type', 'in', ['bank', 'cash'])]))
    payment_type = fields.Selection([('inbound', 'Customer'), ('outbound', 'Supplier')], 'Payment Type')
    pdc_only = fields.Boolean('PDC only')
    effective_date_from = fields.Date('Effective Date From')
    effective_date_to = fields.Date('Effective Date Upto')

    def print_report(self):
        self.ensure_one()
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        return self.env.ref('account_pdc_payment_report.action_report_payment').report_action(self, data=data)






