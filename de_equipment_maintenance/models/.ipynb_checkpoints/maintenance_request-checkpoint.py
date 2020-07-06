# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    category_id = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id', string='Category', store=True, readonly=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', ondelete='restrict', index=True)
    equipment_p =  fields.Char(string="", related='equipment_id.equipment_id', required=False, )
    maintenance_order_ids = fields.One2many('maintenance.order', 'maintenance_request_id', string='Maintenance Order')
    maintenance_count = fields.Integer(string='Maintenance Count', compute='_compute_maintenance_order_ids')
    
    @api.depends('maintenance_order_ids')
    def _compute_maintenance_order_ids(self):
        for order in self:
            order.maintenance_count = len(order.maintenance_order_ids)
    
    @api.multi
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
