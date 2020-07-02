# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class EmployeeOvertime(models.Model):
    """Overtime Model."""

    _name = 'hr.attendance.overtime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'
    _description = "Hr Attendance Overtime"

    def action_cancel(self):
        return self.write({'state': 'cancel'})

    def action_approve(self):
        return self.write({'state': 'approve'})

    # @api.onchange('policy_type')
    # def _onchange_policy_type(self):
    #     for rec in self:
    #         if rec.policy_type == 'week_end':
    #             rec.rate = rec.employee_id.weekend_ot_rate
    #         elif rec.policy_type == 'working_days':
    #             rec.rate = rec.employee_id.weekday_ot_rate
    #         else:
    #             rec.rate = 0.0

    def _onchange_policy_type(self):
        for rec in self:
            employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
            if rec.policy_type == 'week_end':
                if employee.weekend_ot_rate:
                    rec.rate = employee.weekend_ot_rate
                else:
                    rec.rate = 0.0
            if rec.policy_type == 'working_days':
                if employee.weekday_ot_rate:
                    rec.rate = employee.weekday_ot_rate
                else:
                    rec.rate = 0.0
            # if rec.policy_type == 'week_end':
            #     rec.rate = rec.employee_id.weekend_ot_rate
            # elif rec.policy_type == 'working_days':
            #     rec.rate = rec.employee_id.weekday_ot_rate
            # else:
            #     rec.rate = 0.0

    def _compute_employee_attendance(self):
        attendance = self.env['hr.attendance']
        for rec in self:
            rec.attendance_count = attendance.search_count(
                [('employee_id', '=', rec.employee_id.id)])

    def action_view_attendance(self):
        return {
            'name': _('Attendance'),
            'type': 'ir.actions.act_window',
            'domain': [('employee_id', '=', self.employee_id.id)],
            'res_model': 'hr.attendance',
            'view_mode': 'tree,form',
            'view_id': False,
            'context': {}
        }

    name = fields.Char(string='Name')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', track_visibility='always')
    policy_type = fields.Selection([('working_days', 'Working days'),
                                    ('week_end', 'Holidays'),
                                    ('public_holiday', 'Public holiday')],
                                   string='Based On', track_visibility='onchange')
    rate = fields.Float(string='Rate', readonly=True, compute='_onchange_policy_type')
    date = fields.Date(string='Date', required=True, track_visibility='onchange')
    overtime = fields.Float(string='Overtime')
    state = fields.Selection([('draft', 'Draft'),
                              ('approve', 'Approved'),
                              ('paid', 'Paid'),
                              ('cancel', 'Canceled')],
                             string='State')
    notes = fields.Text(string='Notes')
    attendance_id = fields.Many2one('hr.attendance', string='Attendance')
    attendance_count = fields.Integer(compute='_compute_employee_attendance')
