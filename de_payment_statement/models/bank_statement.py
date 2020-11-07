from odoo import api, fields, models, _
from odoo.exceptions import UserError


class account_payment(models.Model):
    _inherit = 'account.payment'

    bank_statement_entry = fields.Boolean(string='Add Bank Statement Entry')
    bank_statement = fields.Many2one('account.bank.statement')

    def post(self):
        data = []
        #         for rec in self.bank_statement.line_ids:
        data.append((0, 0, {
            'date': self.payment_date,
            'name': self.name,
            'partner_id': self.partner_id.id,
            'ref': self.name,
            'amount': self.amount,

        }))
        self.bank_statement.line_ids = data
        return super(account_payment, self).post()

#     @api.model
#     def create(self, vals):
#         data = []
#         record = self.env['account.bank.statement.line'].search(['id','=', self.bank_statement.id])
#         record = self.env['account.payment'].search([])
#         for rec in record:
#             data.append((0, 0, {
#                 'date' : rec.payment_date,
#                 'name' : 'test'
#             }))
#         vals['bank_statement_line'] = data
