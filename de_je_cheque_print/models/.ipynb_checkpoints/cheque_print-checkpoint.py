# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class JeChequePrint(models.Model):
    _inherit = 'account.move'

    is_cheque_print = fields.Boolean(string='Cheque Print', default=False)
    payee = fields.Char(string='Payee')
    amount = fields.Float(string='Amount')
    cheque_format_id = fields.Many2one('cheque.setting', string='Cheque Format')