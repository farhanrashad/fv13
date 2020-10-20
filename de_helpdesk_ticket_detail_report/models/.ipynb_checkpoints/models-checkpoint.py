# -*- coding: utf-8 -*-

from odoo import models, fields, api, _





class ResUsers(models.Model):
    _inherit = 'res.users'

    address = fields.Char(string='Street')

