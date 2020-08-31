# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    sal_limit = fields.Float(string='Advance Salary Request', store =True)
    sal_req_limit = fields.Integer(string='Advance Salary Limit', store=True, required=True)
    

    
    
class EmployeeAdvanceSalary(models.Model):
    _name = 'hr.employee.advance.salary'
    _description = 'HR Employee Advance Salary'
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
        

    name = fields.Char(string='Reference',  copy=False,  index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True, required=True)
    request_date = fields.Date(string='Request Date', store=True, required=True)
    confirm_date = fields.Date(string='Confirm Date', store=True)
    amount = fields.Float(string='Request Amount', store=True, required=True)
    manager_id = fields.Many2one('hr.employee',string='Department Manager', store=True, required=True)
    conf_manager_id = fields.Many2one('hr.employee',string='Confirm Manager', store=True)
#     user_id = fields.Many2one('res.users', string='Issuer', store=True, required=True)
    note = fields.Char(string="Reason" , required = True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('request', 'Request'),
        ('approval', 'Approval'),
        ('hrconfirm', 'HR Confirm'),        
        ('paid', 'Paid'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    department_id = fields.Many2one('hr.department', string='Department')
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('hr.employee.advance.salary') 
        values['name'] = seq
        res = super(EmployeeAdvanceSalary,self).create(values)
        return res