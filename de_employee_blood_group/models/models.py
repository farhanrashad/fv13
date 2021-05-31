# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeBlood(models.Model):
    _inherit = 'hr.employee'
    
    
    
    blood_group = fields.Selection([('O+','O+'),
                                    ('O-','O-'),
                                    ('A+','A+'),
                                    ('A-','A-'),
                                    ('B+','B+'),
                                    ('B-','B-'),
                                    ('AB+','AB+'),
                                    ('AB-','AB-'),
                                   ], string='Blood Group')