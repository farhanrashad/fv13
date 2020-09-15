from odoo import models,fields

class EmployeeInheritence(models.Model):
    _inherit = 'hr.employee'

    emp_location = fields.Char(string="Location")