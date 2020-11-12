from datetime import datetime


from odoo.tools.float_utils import float_compare

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PaymentSchedule(models.Model):
    _name = 'purchase.lease.payment.schedule'
    _description = "Payment Schedule"

    schedule_id = fields.Many2one('purchase.order', string='schedule_id', index=True, ondelete='cascade')
    installment_amount = fields.Float('Installment Amount')
    date = fields.Date("Date")
    invoice_id = fields.Many2one('account.move')
    is_invoiced = fields.Boolean('Is Invoiced?', default=False)


class PurchaseLease(models.Model):
    _inherit = 'res.partner'

    is_landlord = fields.Boolean('Is Landlord?', default=False)


class ContractLease(models.Model):
    _inherit = 'purchase.order'

    def action_view_test(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'object',
            'domain': [('invoice_origin', '=', self.name)],
            'multi': False,
            'name': 'Tasks',
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }

    def get_bill_count(self):
        count = self.env['account.move'].search_count([('name', '=', self.name)])
        self.bill_count = count

    bill_count = fields.Integer(string="Journal Entries", compute='get_bill_count')

    is_lease_contract = fields.Boolean('Is Lease?', default=False)
    lease_type = fields.Many2one('purchase.lease.type', string="Lease Type")
    summary = fields.Text(string="Summary")
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    credit_account_id = fields.Many2one('account.account', string='Credit Account')
    journal_id = fields.Many2one('account.journal', string='Journal')

    recurring_period = fields.Selection([
        ('days', 'Day(s)'),
        ('weeks', 'Week(s)'),
        ('months', 'Month(s)'),
        ('years', 'Year(s)'),
    ], string='Recurring Period', copy=False, index=True, tracking=3, default='months')

    invoiced_amount = fields.Float('Invoiced Amount', readonly=1)
    remaining_amount = fields.Float('Remaining Amount', compute="compute_remaining_amount", readonly=1)
    schedule_lines = fields.One2many('purchase.lease.payment.schedule', 'schedule_id', string='Activity Schedule line',
                                     copy=True, auto_join=True)

    def action_create_lease_bills(self):
        line_vals = []
        for line in self.order_line:
            line_vals.append((0,0, {
#                  'move_id': move.id,
                 'product_id': line.product_id.id,
                 'name':line.product_id.name,
                 'account_id': self.credit_account_id.id,
                 'quantity': line.product_qty,
                 'currency_id': line.currency_id.id, 
                 'price_unit': line.price_unit,
                 'partner_id': self.partner_id.id,
                 'product_uom_id': line.product_uom.id,
            }))
            line_vals.append(line_vals)
            
            vals = {
            'partner_id': self.partner_id.id,
            'journal_id': self.journal_id.id,
            'invoice_date': fields.Date.today(),
            'type': 'in_invoice',
            'invoice_origin': self.name,
            'invoice_line_ids': line_vals    
             }
        move = self.env['account.move'].create(vals)
# #             self.ensure_one()
#             if line.product_id.purchase_method == 'purchase':
#                 qty = line.product_qty
#             else:
#                 qty = line.product_qty
#             if float_compare(qty, 0.0, precision_rounding=line.product_uom.rounding) <= 0:
#                 qty = 0.0

#             if line.currency_id == move.company_id.currency_id:
#                 currency = False
#             else:
#                 currency = move.currency_id

#             return {
#                 'name': '%s: %s' % (line.order_id.name, line.name),
#                 'move_id': move.id,
#                 'currency_id': currency and currency.id or False,
#                 'purchase_line_id': line.id,
#                 'date_maturity': move.invoice_date_due,
#                 'product_uom_id': line.product_uom.id,
#                 'product_id': line.product_id.id,
#                 'price_unit': line.price_unit,
#                 'quantity': qty,
#                 'partner_id': move.partner_id.id,
#                 'analytic_account_id': line.account_analytic_id.id,
#                 'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
#                 'tax_ids': [(6, 0, line.taxes_id.ids)],
#                 'display_type': line.display_type,
#             }

#         print("Invoice Generation Called")
# #         for record in self:
# #         record = self.env['purchase.order'].search([('is_lease_contract', '=', True), ('state', '=', 'purchase')])
#         current_date = datetime.today().date()

#         for rec in self:
#             for line in self.schedule_lines:
#                 if line.date == current_date:
#                     val = {
#                         'partner_id': rec.partner_id.id,
#                         'journal_id': 58,
#                         'invoice_origin': rec.name,
#                         'invoice_date': line.date,
#                         'purchase_id': rec.name,
# #                         'date': line.date,
# #                         'state': 'draft',
# #                         'invoice_date_due': line.date,
#                         'type': 'in_invoice',
#                     }
#                     account_move = self.env['account.move'].create(val)
#                     for order in rec.order_line:
#                         vals = {
#                             'move_id': account_move.id,
# #                             'display_type': order.display_type,
# #                             'sequence': order.sequence,
#                             'product_id': order.product_id.id,
#                             'name': order.name,
#                             'account_id': rec.credit_account_id.id,
# #                             'date': order.date_planned,
# #                             'quantity': order.product_qty,
#                             'price_unit': 100,
# #                             'tax_ids': order.taxes_id.id,
# #                             'currency_id': rec.currency_id.id,
# #                             'tax_line_id': order.taxes_id,
# #                             'price_subtotal': order.price_subtotal,
# #                             'parent_state': account_move.state,
#                             'product_uom_id': order.product_id.uom_id.id,
# #                             'company_id': rec.company_id.id,
#                             'partner_id': rec.partner_id.id,
# #                             'ref': rec.partner_ref,
# #                             'purchase_line_id': order.id,
#                         }
#                         account_move_line = self.env['account.move.line'].create(vals)
#                         print("Invoice generated")

                        
#                         order.product_id.property_account_expense_id.id


#         for rec in self:
#             current_date = datetime.today().date()
#             for line in rec.schedule_lines:
#                 # print(line.is_invoiced, current_date, line.date)
#                 if line.date == current_date and line.is_invoiced == False:
#                     line_ids = []
#                     debit_sum = 0.0
#                     credit_sum = 0.0
#                     move_dict = {
#                         'name': self.name,
#                         'journal_id': rec.journal_id.id,
#                         'date': line.date,
#                         'state': 'draft',
# #                         'move_type': 'in_invoice',
#                         'invoice_origin': self.name,
#                     }
#                     for oline in rec.order_line:
#                         debit_line = (0, 0, {
#                             # 'move_id': move_dict.id,
#                             'name': oline.name,
#                             'debit': float(abs(line.installment_amount)),
#                             'credit': 0.0,
#                             'account_id': rec.credit_account_id.id,
#                             'product_id': oline.product_id.id,

#                         })
#                         line_ids.append(debit_line)
#                         debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
#                         # step3:credit side entry
#                         credit_line = (0, 0, {
#                             'name': oline.name,
#                             'debit': 0.0,
#                             'credit': abs(line.installment_amount),
#                             'account_id': rec.credit_account_id.id,
#                             'product_id': oline.product_id.id,
#                         })
#                         # print(line_ids)
#                         line_ids.append(credit_line)
#                         credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

#                     move_dict['line_ids'] = line_ids
#                     move = self.env['account.move'].create(move_dict)
#                     # invoiced_dict = {
#                     #     'schedule_id': rec.id,
#                     #     'is_invoiced': 'True',
#                     # }
#                     # invoiced_move = self.env['purchase.lease.payment.schedule'].create(invoiced_dict)
#                     print('General entry created')

#                 else:
#                     print('Not found or Invoice Already Generated!!!!')

    def button_cancel(self):
        print('Scheduler Stopped!!!!!!!!')
        result = super(ContractLease, self).button_cancel()
        scheduler = self.env['ir.cron'].search([('name', '=', 'Activity Scheduler')])
        if not scheduler:
            scheduler = self.env['ir.cron'].search(
                [('name', '=', 'Activity Scheduler'), ('active', '=', False)])
        scheduler.active = False

    def button_confirm(self):
        print('Inside Function!!!!!!!!!!!')
        result = super(ContractLease, self).button_confirm()
        try:
            self.compute_recurring_period()
            print('Scheduler is Running!!!!!!!!!!!')
            scheduler = self.env['ir.cron'].search([('name', '=', 'Activity Scheduler')])
            if not scheduler:
                scheduler = self.env['ir.cron'].search(
                    [('name', '=', 'Activity Scheduler'), ('active', '=', False)])
            scheduler.active = True
            scheduler.interval_number = 1
            scheduler.interval_type = 'days'
        except:
            raise UserError(_('Error on Confirm Button'))

    def compute_recurring_period(self):
        data = []
        for line in self.schedule_lines:
            line.unlink()

        for rec in self:
            delta = rec.start_date - rec.end_date
            total_days = abs(delta.days)
            if total_days > 0:
                if self.recurring_period == 'months':
                    months = int(total_days / 30)
                    invoice_amount = rec.amount_total / months
                    for i in range(0, months):
                        i = i + 1
                        date_after_month = self.start_date + relativedelta(months=i)
                        data.append((0, 0, {
                            'installment_amount': invoice_amount,
                            'date': date_after_month,
                            'invoice_id': '',
                            'schedule_id': rec.id,
                        }))
                    self.schedule_lines = data

                elif self.recurring_period == 'years':
                    years = int(total_days / 365)
                    invoice_amount = rec.amount_total / years
                    for i in range(0, years):
                        i = i + 1
                        date_after_month = self.start_date + relativedelta(years=i)
                        data.append((0, 0, {
                            'installment_amount': invoice_amount,
                            'date': date_after_month,
                            'invoice_id': '',
                            'schedule_id': rec.id,
                        }))
                    self.schedule_lines = data

                elif self.recurring_period == 'weeks':
                    weeks = int(total_days / 7)
                    invoice_amount = rec.amount_total / weeks
                    for i in range(0, weeks):
                        i = i + 1
                        date_after_month = self.start_date + relativedelta(weeks=i)
                        data.append((0, 0, {
                            'installment_amount': invoice_amount,
                            'date': date_after_month,
                            'invoice_id': '',
                            'schedule_id': rec.id,
                        }))
                    self.schedule_lines = data

                elif self.recurring_period == 'days':
                    invoice_amount = rec.amount_total / total_days
                    for i in range(0, total_days):
                        i = i + 1
                        date_after_month = self.start_date + relativedelta(days=i)
                        data.append((0, 0, {
                            'installment_amount': invoice_amount,
                            'date': date_after_month,
                            'invoice_id': '',
                            'schedule_id': rec.id,
                        }))
                    self.schedule_lines = data

    def compute_remaining_amount(self):
        for rec in self:
            rec.remaining_amount = rec.amount_total - rec.invoiced_amount


class LandProperty(models.Model):
    _inherit = 'project.project'

    is_property = fields.Boolean(default=False)
    property_type_id = fields.Many2one('purchase.property.type')
    address_id = fields.Many2one('res.partner', string="Address")
    google_longitude = fields.Char("Google Longitude")
    google_latitude = fields.Char("Google Latitude")
    landlord_id = fields.Many2one('res.partner', string="Landlord")


class Checklist(models.Model):
    _name = 'purchase.checklist.activity'
    _description = 'Purchase Checklist'

    activity_id = fields.Many2one('mail.activity')

    state = fields.Selection([
        ('todo', 'To-Do'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='todo')


class PropertyType(models.Model):
    _name = 'purchase.property.type'
    _description = 'Property Type'

    property_type = fields.Char('Name')


class LeaseType(models.Model):
    _name = 'purchase.lease.type'
    _description = 'Lease Type'

    name = fields.Char(string='Name')
