# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from num2words import num2words


class JeChequePrint(models.Model):
    _inherit = 'account.move'

    is_cheque_print = fields.Boolean(string='Cheque Print', default=False)
    payee = fields.Char(string='Payee')
    amount = fields.Float(string='Amount')
    cheque_formate_id = fields.Many2one('cheque.setting', string='Cheque Format')
    
    
    @api.model
    def get_date(self,date):
        print('=========================',date)
        date = str(date).split('-')
        print('=========================',date)
        return date
    
    @api.model
    def amount_word(self, obj):
        amt_word = num2words(obj.amount)
        
        return amt_word