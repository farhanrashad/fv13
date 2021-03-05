# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class JeChequePrint(models.Model):
    _inherit = 'account.move'

    is_cheque_print = fields.Boolean(string='Cheque Print', default=False)