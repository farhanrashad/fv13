# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#

##############################################################################
from odoo import models,fields, api
from odoo import tools

class account_voucher(models.Model):
    _inherit ='account.payment'
    
    @api.onchange('partner_id')
    def onchange_partner(self):
        self.pay_by = self.partner_id.name

    cheque_formate_id = fields.Many2one('cheque.setting', 'Cheque Formate', required=True)
    cheque_no = fields.Char('Cheque No')
    text_free = fields.Char('Free Text')
    partner_text = fields.Char('Partner Title')
    pay_by = fields.Char(string='Pay By', store=True)
    
    
        

    def do_print_checks(self):
        return self.env.ref('dev_print_cheque.action_report_print_cheque').report_action(self)


    
# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:    
