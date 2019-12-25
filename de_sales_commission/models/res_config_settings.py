# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    commission_percentage = fields.Float("Default Commission Percentage",
                                         config_parameter='agent.commission')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            commission_percentage=self.env['ir.config_parameter'].sudo().get_param('agent.commission'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('agent.commission', self.commission_percentage)



