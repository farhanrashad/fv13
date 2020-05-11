# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_estimate_new_crm(self):
        if not self.partner_id:
            return self.env.ref("de_sales_estimation.crm_estimate_partner_action").read()[0]
        else:
            return self.action_new_estimate_crm()

    def action_new_estimate_crm(self):
        action = self.env.ref("de_sales_estimation.estime_action_quotations_new").read()[0]
        action['context'] = {
            'search_default_partner_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_est_team': self.team_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_est_user_id': self.user_id.id,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
        }
        return action

    def open_sale_estimates(self):
        self.ensure_one()

        return {
            'name': 'Estimate',
            'view_id': False,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sales.estimate',
            'type': 'ir.actions.act_window',
            # 'domain': [],
            # 'context': "{'create': True}"
        }

    def estimate_count(self):
        count = self.env['sales.estimate'].search_count([('opportunity_id', '=', self.id)])
        self.estimate_count_id = count

    estimate_count_id = fields.Integer(string="Estimate", compute="estimate_count")
    
    estimation_count = fields.Integer(compute='_compute_estimate_data', string="Number of Estimations")
    estimate_ids = fields.One2many('sales.estimate', 'opportunity_id', string='Orders')
    
    #@api.depends('estimate_ids.state',  'order_ids.amount_untaxed', 'order_ids.date_order', 'order_ids.company_id')
    def _compute_estimate_data(self):
        for lead in self:
            total = 0.0
            estimation_cnt = 0
            
            for est in lead.estimate_ids:
                if est.state not in ('cancel'):
                    estimation_cnt += 1
            lead.estimation_count = estimation_cnt
            
    def action_view_estimation(self):
        action = self.env.ref('sale_estimates_tree').read()[0]
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id
        }
        action['domain'] = [('opportunity_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]
        quotations = self.mapped('estimate_ids').filtered(lambda l: l.state in ('draft', 'sent'))
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale_estimates_form').id, 'form')]
            action['res_id'] = quotations.id
        return action


