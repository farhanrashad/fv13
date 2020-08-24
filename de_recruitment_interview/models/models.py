# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class EmployeeInterviewAssessment(models.Model):
    _name = 'hr.employee.interview.assessment'
    _description = 'HR Employee Interview Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'
    
    @api.onchange('name')
    def onchange_name(self):
        
        user_obj = self.env['hr.employee.interview.assessment.line'].search([])
        if self.name:
            for rec in user_obj:
                data = []
                data.append((0,0,{
                        'name': rec.name,
                        'scope': rec.scope,
                        'remarks': rec.remarks,
                        'interview_id': self.id
                        }))
                self.assessment_ds = data 


    name = fields.Char(string='Order Reference',  copy=False,  index=True, required=True)
    position_id = fields.Many2one('hr.applicant', string='Position', store=True, required=True)
    date = fields.Date(string='Date', store=True)
    phone = fields.Char(string='Phone', store=True, related='position_id.partner_phone')
    address = fields.Char(string='Address')
    business_type = fields.Char(string='Type of Business')
    work = fields.Char(string='Family/Friend Working in Company')
    notice_period = fields.Char(string='Notice Period')
    age = fields.Char(string='Age', store=True)
    department_id = fields.Many2one('hr.department', store=True, related='position_id.department_id')
    family_origin = fields.Char(string="Family Origin")
    martial_status = fields.Selection([
        ('married', 'Married'),
        ('single', 'Single'),
    ], string='Martial Status',  copy=False, index=True, default='single')
    last_job = fields.Char(string='Last Job')
    strength = fields.Char(string='Strengths')
    weakness = fields.Char(string='Weakness')
    comments = fields.Char(string='Overall Comments and Recomendations')
    suit_recruit = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='SUITABILITY TO RECRUIT',  copy=False, index=True, default='yes')
    suit_develop = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='POTENTIAL TO DEVELOP',  copy=False, index=True, default='yes')
    recruit_reservation = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='RESERVATION', copy=False, index=True, default='yes')
    develop_reservation = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='RESERVATION',  copy=False, index=True, default='yes')
    interviewer_id = fields.Many2one('res.users', string='INTERVIEWER', store=True)
    date = fields.Date(string='Date', store=True)   
    assessment_ds = fields.One2many('hr.employee.interview.assessment.line', 'interview_id',)


    
    
    class EmployeeInterviewAssessmentLine(models.Model):
        _name = 'hr.employee.interview.assessment.line'
        _description = 'HR Employee Interview Assessment Line'

        interview_id = fields.Many2one('hr.employee.interview.assessment', string='Interview', store=True)
        name = fields.Char(string='Criteria',  copy=False,  index=True)
        scope = fields.Float(string='Scope (1-5)', store=True, size=5)
        remarks = fields.Char(string='Remarks', store=True)
        
        @api.constrains('scope')
        def _check_value(self):
            if self.scope > 0.0 or self.field_name <= 5.0:
                raise ValidationError(_('Enter Scope Value Between 0-5.'))
    
#     @api.model
#     def create(self,values):
#         seq = self.env['ir.sequence'].get('hr.employee.disciplinary.case') 
#         values['name'] = seq
#         res = super(EmployeeDesciplinaryCase,self).create(values)
#         return res