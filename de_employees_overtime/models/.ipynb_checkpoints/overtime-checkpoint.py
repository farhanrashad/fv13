# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.department'
    
    allow_overtime = fields.Boolean(string="Allow Overtime", store=True)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    allow_overtime = fields.Boolean(related='department_id.allow_overtime', store=True)
    
    
    
    
class EmployeeOvertime(models.Model):
    _name = 'hr.employee.overtime'
    _description = 'Employee Overtime'

    name = fields.Many2one('hr.employee', string="Employee", store=True)
    date = fields.Date(string='Date', required=True)
    check_in = fields.Date(string="Check In", readonly=True)
    check_out = fields.Date(string="Check Out", readonly=True)
    total_hours = fields.Integer(string="Total Hours", readonly=True)
    overtime_hours = fields.Integer(string="Overtime Hours", readonly=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('to_approve', 'To Approve'),
        ('refused', 'Refused'),
        ('approved', 'Approved'),        
        ('paid', 'Paid'),
        ('close', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    

    
class EmployeeOvertimeRule(models.Model):
    _name = 'hr.employee.overtime.rule'
    _description = 'Employee Overtime Rule'
    _rec_name = 'overtime_type_id'

    department_id = fields.Many2one('hr.department', string="Department", store=True)
    overtime_type_id = fields.Many2one('hr.employee.overtime.type', string="Overtime Type", store=True)
    employee_ids = fields.Many2many('hr.employee', string="Employee", store=True)
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string="Date To")
    overtime_hours = fields.Integer(string="Allow Overtime Hours", required=True)
    type = fields.Selection(selection=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ], string='Type', required=True, store=True, index=True, readonly=True, tracking=True,
        default="yearly")
    overtime_type = fields.Selection(selection=[
            ('fixed', 'Fixed'),
            ('percent', 'Percentage'),
        ], string='Type', required=True, store=True, index=True, readonly=True, tracking=True,
        default="fixed")
    
    
class EmployeeOvertimeRule(models.Model):
    _name = 'hr.employee.overtime.type'
    _description = 'Employee Overtime Type'

    name = fields.Char(string="Name", store=True)    

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
