# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EmployeeDesciplinaryCaseType(models.Model):
    _name = 'hr.employee.disciplinary.case.type'
    _description = 'HR Employee Desciplinary Case type'
    _order = 'name desc'


    name = fields.Char(string='Name', store=True, required=True)
    

    
class EmployeeDesciplinaryCase(models.Model):
    _name = 'hr.employee.disciplinary.case'
    _description = 'HR Employee Desciplinary Case'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'
    
    def action_case_send(self):
        template_id = self.env.ref('de_employee_disciplinary_case.email_template_edi_disciplinary_case').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.write({
            'state': 'response',
        })    
        
    def action_waiting_case(self):
        self.write({
            'state': 'waiting',
        })    
       
    def action_close_case(self):
        self.write({
            'state': 'close',
        })    
        

    name = fields.Char(string='Order Reference',  copy=False,  index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True)
    date = fields.Date(string='Date', store=True)
    case_type = fields.Many2one('hr.employee.disciplinary.case.type',string='Case Type', store=True)
    user_id = fields.Many2one('res.users', string='Issuer', store=True, required=True)
    note = fields.Html(string="Description" )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('response', 'Response'),
        ('close', 'Close'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('hr.employee.disciplinary.case') 
        values['name'] = seq
        res = super(EmployeeDesciplinaryCase,self).create(values)
        return res


    