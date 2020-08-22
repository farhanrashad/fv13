# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EmployeeInterviewAssessment(models.Model):
    _name = 'hr.employee.interview.assessment'
    _description = 'HR Employee Interview Assessment'
    _order = 'name desc'


    name = fields.Char(string='Order Reference',  copy=False,  index=True)
    position_id = fields.Many2one('hr.applicant', string='Position', store=True)
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
    ], string='Martial Status', readonly=True, copy=False, index=True, default='single')
    last_job = fields.Char(string='Last Job')
    strength = fields.Char(string='Strengths')
    weakness = fields.Char(string='Weakness')
    comments = fields.Char(string='Overall Comments and Recomendations')
    suit_recruit = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='SUITABILITY TO RECRUIT', readonly=True, copy=False, index=True, default='yes')
    suit_develop = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='POTENTIAL TO DEVELOP', readonly=True, copy=False, index=True, default='yes')
    recruit_reservation = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='RESERVATION', readonly=True, copy=False, index=True, default='yes')
    develop_reservation = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO'),
    ], string='RESERVATION', readonly=True, copy=False, index=True, default='yes')
    interviewer_id = fields.Many2one('res.users', string='INTERVIEWER', store=True)
    date = fields.Date(string='Date', store=True)
    
    assessment_ds = fields.Many2many('hr.employee.interview.assessment.line', 'interview_id', 'criteria', 'scope', 'remarks')


    
    
    class EmployeeInterviewAssessmentLine(models.Model):
    _name = 'hr.employee.interview.assessment.line'
    _description = 'HR Employee Interview Assessment Line'

    interview_id = fields.Many2one('hr.employee.interview.assessment', string='Interview', store=True)
    name = fields.Char(string='Criteria',  copy=False,  index=True)
    scope = fields.Char(string='Scope (1-5)', store=True)
    remarks = fields.Char(string='Remarks', store=True)
    
    
#     @api.model
#     def create(self,values):
#         seq = self.env['ir.sequence'].get('hr.employee.disciplinary.case') 
#         values['name'] = seq
#         res = super(EmployeeDesciplinaryCase,self).create(values)
#         return res