# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrCourse(models.Model):
    _name = 'training.course'
    _description = 'Model for Hr Training Course'
    _rec_name = 'title'

    @api.model
    def create(self, vals):
        if vals.get('course_seq', _('No ID')) == _('No ID'):
            vals['course_seq'] = self.env['ir.sequence'].next_by_code('hr.training.course') or _(
                'No ID')
            result = super(HrCourse, self).create(vals)
            return result

    title = fields.Char(string='Title')
    coordinator = fields.Many2one('hr.employee', string="Coordinator", required=True, index=True)
    company = fields.Many2one('res.partner', string='Company')
    currency = fields.Many2one('res.currency', string='Currency')
    cost = fields.Char(string='Cost')
    duration = fields.Float(string='Duration')
    description = fields.Text(string='Description')
    course_seq = fields.Char(string='Course ID', required=True, Readonly=True, copy=False, index=True,
                             default=lambda self: _('No ID'))
