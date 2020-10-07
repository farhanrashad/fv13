# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class DisableNegativeStock(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        code = self.picking_type_id.code
        if code == 'incoming':
            delivery_orders = self.env['stock.picking'].search([('origin', '=', self.name)])
            for order in delivery_orders:
                if order.state != 'done':
                    raise UserError(_('Please make sure you have sent the required products to your subcontractor.'))
                else:
                    return super(DisableNegativeStock, self).button_validate()
        else:
            return super(DisableNegativeStock, self).button_validate()
