# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class HrEmployeeExt(models.Model):
    _inherit = 'hr.employee'

    def _compute_count_all(self):
        overtime = self.env['hr.attendance.overtime']
        for rec in self:
            rec.overtime_count = overtime.search_count(
                [('employee_id', '=', rec.id), ('state', '=', 'approve')])

    def open_employee_overtime(self):
        return {
            'name': _('Overtime'),
            'type': 'ir.actions.act_window',
            'domain': [('employee_id', '=', self.id)],
            'res_model': 'hr.attendance.overtime',
            'view_mode': 'tree,form',
            'view_id': False,
            'context': {}
        }

    overtime_cost = fields.Many2one(comodel_name='resource.calendar', string='Working Hours', default=0.0)
    weekday_ot_rate = fields.Float(string='Weekday OT Rate')
    weekend_ot_rate = fields.Float(string='Weekend OT Rate')
    overtime_count = fields.Integer(compute='_compute_count_all')
