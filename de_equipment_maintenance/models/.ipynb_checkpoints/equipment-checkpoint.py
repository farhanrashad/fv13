# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    equipment_id = fields.Many2one(
        'maintenance.equipment', 'Parent Equipment', index=True, ondelete='cascade',
        help="The parent Equipment that includes this equipment. Example : The 'Dispatch Zone' is the 'Gate 1' parent location.")
    child_ids = fields.One2many('maintenance.equipment', 'equipment_id', 'Contains')
    complete_name = fields.Char("Full Equipment Name", compute='_compute_complete_name', store=True)
    
    @api.one
    @api.depends('name', 'equipment_id.complete_name')
    def _compute_complete_name(self):
        """ Forms complete name of equpment from parent equipment to child equipment. """
        if self.equipment_id.complete_name:
            self.complete_name = '%s/%s' % (self.equipment_id.complete_name, self.name)
        else:
            self.complete_name = self.name