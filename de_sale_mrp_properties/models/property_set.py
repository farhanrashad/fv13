# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PropertySetValue(models.Model):
    _name = 'property.value'
    _description = 'Property Value'
    _rec_name = 'value'

    value = fields.Char(string='Value')


class MrpProductionPropertySet(models.Model):
    _name = 'mrp.production.property.set'
    _description = 'MRP Production Property Set'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    value = fields.Many2many(comodel_name='property.value', string='Value')
