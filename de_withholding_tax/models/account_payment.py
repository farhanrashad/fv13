# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountPaymentWHT(models.Model):
    _inherit = 'account.payment'
        
        
    is_wht_liable = fields.Boolean(string='Liable')
    #wht_type_id = fields.Many2one('account.wht_id',string='Withholding Tax Type', required=True, )
    #base_amount = fields.Float(string='Base Amount',required=True)
    #wht_amount = fields.Float(string='WHT Amount',required=True)
    
    #@api.onchange('partner_id')
    #def _onchange_partner_id(self):
        #res = super(AccountPaymentWHT,self)._onchange_partner_id
        #self.is_wht_liable = self.partner_id.is_liable
        #return res