# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class MrpProductionProperties(models.Model):
    _name = 'mrp.production.properties'
    _description = 'MRP Production Properties'
    _rec_name = 'property_id'

    property_id = fields.Many2one(comodel_name='mrp.production.property.set', string='Property Set')
    value_id = fields.Many2one(comodel_name='property.value', string='Tag Ids')
    sale_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    production_id = fields.Many2one(comodel_name='mrp.production', string='Production Id')

    @api.onchange('property_id')
    def onchange_category(self):
        return {'domain': {'value_id': [('id', 'in', self.property_id.value.ids)]}, }
