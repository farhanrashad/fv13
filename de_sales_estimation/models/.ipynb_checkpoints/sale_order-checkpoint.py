# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp

class SaleOrderLineInhert(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLineInhert, self).product_id_change()
        for line in self:
            print("Yess.........", line)
        return res
    
class SaleOrderInhert(models.Model):
    _inherit = 'sale.order'

    estimate_id = fields.Many2one(comodel_name="sales.estimate", string="Estimate", required=False, )

        
    def action_sale_quotations(self):
        if not self.partner_id:
            return self.env.ref("de_sales_estimation.crm_quotation_partner_action").read()[0]
        else:
            return self.action_new_quotation_new()

    def action_new_quotation_new(self):
        action = self.env.ref("de_sales_estimation.sale_action_quotations_new").read()[0]
        action['context'] = {
            # 'search_default_opportunity_id': self.id,
            # 'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_payment_terms_id': self.payment_terms_id,
            'default_team_id': self.est_team.id,
            'default_order_line': self.est_order_line.id,
            # 'default_campaign_id': self.campaign_id.id,
            # 'default_medium_id': self.medium_id.id,
            # 'default_origin': self.name,
            # 'default_source_id': self.source_id.id,
            # 'default_company_id': self.company_id.id or self.env.company.id,
        }
        return action

    @api.onchange('est_src')
    def onchange_method(self):
        for rec in self:
            line = []
            for line in self.order_line.est_order_line:
                vals = {
                    'est_src': line.id
                }
            line.append(0, 0, vals)
        print("lines", line)
        # rec.order_line = line
