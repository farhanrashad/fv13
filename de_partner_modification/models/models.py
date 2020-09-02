# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PartnerModification(models.Model):
    _name = 'res.partner'
    
    def _get_default_stage_id(self):
        return self.env['partner.stages'].search([], limit=1).id
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['partner.stages'].search([])
        return stage_ids

    stage_id = fields.Many2one('partner.stages', string='Stage', ondelete='restrict', tracking=True, index=True,
         group_expand='_read_group_stage_ids',
          default=_get_default_stage_id,
         copy=False)
    
    
class PartnerStages(models.Model):
    _name = 'partner.stages'
    _description = 'Partner Stage'
    
    

    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    active = fields.Boolean(default=True)
    unattended = fields.Boolean(
        string='Unattended')
    closed = fields.Boolean(
        string='Closed')
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Email Template',
        domain=[('model', '=', 'helpdesk.ticket')],
        help="If set an email will be sent to the "
             "customer when the ticket"
             "reaches this step.")
    fold = fields.Boolean(
        string='Folded in Kanban',
        help="This stage is folded in the kanban view "
             "when there are no records in that stage "
             "to display.")
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'helpdesk.ticket')
    )    