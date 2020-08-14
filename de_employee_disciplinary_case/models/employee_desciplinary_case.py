# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EmployeeDesciplinaryCaseType(models.Model):
    _name = 'hr.employee.disciplinary.case.type'
    _description = 'HR Employee Desciplinary Case type'

    name = fields.Char(string='Name', store=True, required=True)
    

    
class EmployeeDesciplinaryCase(models.Model):
    _name = 'hr.employee.disciplinary.case'
    _description = 'HR Employee Desciplinary Case'

    name = fields.Char(string='Name', store=True, required=True)
    employee_id = fields.