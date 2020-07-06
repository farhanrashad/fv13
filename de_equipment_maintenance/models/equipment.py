# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    equipment_id = fields.Many2one(
        comodel_name='maintenance.equipment', string='Parent Equipment', index=True, ondelete='cascade')
    child_ids = fields.One2many(comodel_name='maintenance.equipment', inverse_name='equipment_id', string='Contains')
    complete_name = fields.Char(string='Full Equipment Name', compute='_compute_complete_name', store=True)
    owner_user_id = fields.Many2one(comodel_name='res.users', string='Owner', track_visibility='onchange')
    maintenance_team_id = fields.Many2one(comodel_name='maintenance.team', string='Maintenance Team')

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        self.complete_name = self.equipment_id.complete_name

    @api.depends('name', 'equipment_id.complete_name')
    def _compute_complete_name(self):
        self.ensure_one()
        """ Forms complete name of equpment from parent equipment to child equipment. """
        if self.equipment_id.complete_name:
            self.complete_name = '%s/%s' % (self.equipment_id.complete_name, self.name)
        else:
            self.complete_name = self.name
