# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api, _


class EmployeePayslipExt(models.Model):
    _inherit = 'hr.payslip'

    overtime_ids = fields.One2many(comodel_name='employee.payslip.overtime', inverse_name='overtime_id')

    def overtime_calculation(self):
        cost = 0.0
        overtime_data = self.env['employee.payslip.overtime'].search([('overtime_id', '=', self.id)])
        for delta in overtime_data:
            cost = cost + delta.rate
        return cost

    def action_payslip_done(self):
        res = super(EmployeePayslipExt, self).action_payslip_done()
        to_paid = self.env['hr.attendance.overtime'].search([('employee_id', '=', self.employee_id.id),
                                                   ('state', '=', 'approve')])
        for pay in to_paid:
            pay.write({'state': 'paid'})
        return res


class EmployeePayslipOvertime(models.Model):
    _name = 'employee.payslip.overtime'
    _description = 'Employee Payslip Overtime'

    overtime_id = fields.Many2one(comodel_name='hr.payslip', string='Overtime Id')
    policy_type = fields.Selection([('working_days', 'Working days'),
                                    ('week_end', 'Holidays'),
                                    ('public_holiday', 'Public holiday')],
                                   string='Based On')
    rate = fields.Float(string='Rate')
    date = fields.Date(string='Date', required=True)
    overtime = fields.Float(string='Overtime')
