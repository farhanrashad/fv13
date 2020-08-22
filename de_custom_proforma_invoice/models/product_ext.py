# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductProductExt(models.Model):
    _inherit = 'product.product'

    item_style = fields.Char(string='Style')
    item_color = fields.Char(string='Color')
    item_order = fields.Char(string='Order')
    hs_code = fields.Char(string='Hs Code')
    composition = fields.Char(string='Composition')
