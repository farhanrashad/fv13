# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    order_category = fields.Char(string="Order Category")
