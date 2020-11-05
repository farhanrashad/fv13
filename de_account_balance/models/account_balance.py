# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

class AccountBalance(models.Model):
    _inherit = 'res.partner'

    balance = fields.Monetary(string='Balance', compute='_compute_balance', store=True,)

    @api.depends('debit', 'credit')
    def _compute_balance(self):
        for line in self:
            line.balance = line.debit - line.credit
