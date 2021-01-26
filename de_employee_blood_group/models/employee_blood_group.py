# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HrEmployeeBlood(models.Model):
    _inherit = 'hr.employee'

    blood_group = fields.Selection([('O+','O+'),
                                ('O-','O-'),
                                ('A+','A+'),
                                ('A-','A-'),
                                ('B+','B+'),
                                ('B-','B-'),
                                ('AB+','AB+'),
                                ('AB-','AB-'),],'Blood Group')