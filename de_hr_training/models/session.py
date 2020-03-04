# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrSession(models.Model):
    _name = 'training.session'
    _description = 'This is a model for Sessions in HR Training Module'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    def action_quotation_approve(self):
        self.state = 'done'
        return True

    def apply_state(self):
        for rec in self:
            rec.state = 'confirm'

    def pending_state(self):
        for rec in self:
            rec.state = 'done'

    def approve_state(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('session_seq', _('No ID')) == _('No ID'):
            vals['session_seq'] = self.env['ir.sequence'].next_by_code('hr.training.session') or _(
                'No ID')
            result = super(HrSession, self).create(vals)
            return result

    name = fields.Char(string='Name', required=True)
    course = fields.Many2one('training.course', required=True, string='Course')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    delivery_location = fields.Char(string='Delivery Location')
    delivery_method = fields.Selection([('classroom', 'Classroom'), ('self_study', 'Self Study')],
                                       string='Delivery Method')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Applied'),
        ('confirm', 'Pending Approval'),
        ('done', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', track_visibility='onchange')
    session_seq = fields.Char(string='Session ID', required=True, Readonly=True, copy=False, index=True,
                              default=lambda self: _('name'))
