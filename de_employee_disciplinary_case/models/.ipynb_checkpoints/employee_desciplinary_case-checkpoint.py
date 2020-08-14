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
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True)
    date = fields.Date(string='Date', store=True)
    case_type = fields.Many2one('hr.employee.disciplinary.case.type',string='Case Type', store=True)
    user_id = fields.Many2one('res.user', string='Issuer', store=True, required=True)
    note = fields.Html(string="Description" )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('response', 'Response'),
        ('close', 'Close'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    attachment_id = fields.Many2one('ir.attachment', string="Attachment", required=True)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    test = fields.Char(string='Name', store=True, required=True)
    