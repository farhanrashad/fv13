# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment',
                                   ondelete='restrict', index=True)
    owner_user_id = fields.Many2one('res.users', string='Owner', track_visibility='onchange')
    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team')
    pfiled = fields.Many2one(comodel_name="maintenance.equipment", related='equipment_id.equipment_id', string="Parent Equipment", required=False, )

    # @api.onchange('equipment_id')
    # def _onchange_equipment_id(self):
    #     for rec in self:
    #         if rec.equipment_id.equipment_id.name:
    #             rec.pfiled = rec.equipment_id.equipment_id.id

    # @api.onchange('equipment_id')
    # def _onchange_equipment_id(self):
    #     for rec in self:
    #         if rec.equipment_id.equipment_id:
    #             rec.pfiled = rec.equipment_id.equipment_id.id



        # self.maintenance_team_id = self.equipment_id.maintenance_team_id

    maintenance_order_ids = fields.One2many('maintenance.order', 'maintenance_request_id', string='Maintenance Order')
    maintenance_count = fields.Integer(string='Maintenance Count', compute='_compute_maintenance_order_ids')
    
    @api.depends('maintenance_order_ids')
    def _compute_maintenance_order_ids(self):
        for order in self:
            order.maintenance_count = len(order.maintenance_order_ids)

    def action_view_order(self):
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi':False,
            'name': 'Maintenance Order',
            'target':'current',
            'res_model': 'maintenance.order',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('maintenance_request_id', '=', self.id)],
            'context': dict(self._context, create=False, default_maintenance_request_id=self.id),
        }


class MaintenanceCost(models.Model):
    _name = 'maintenance.cost'
    _description = "Maintenance Cost"
