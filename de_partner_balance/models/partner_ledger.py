# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################

import time

from odoo import fields, api, models
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class PartnerLedger(models.TransientModel):

    _name = 'partner.balance'

    start_date = fields.Date(
        string='From Date',
        required=True
        #default=lambda *a: (parser.parse(datetime.now().date))
    )
    end_date = fields.Date(
        string='To Date',
        required=True
        # default=lambda *a: (parser.parse(datetime.now().date))
    )
    #is_vendor = fields.Boolean('Vendor Balances', default=False)
    #is_customer = fields.Boolean('Customer Balances', default=False)
    partner_type = fields.Selection([
        ('supplier', 'Vendor Balances'),
        ('customer', 'Customer Balances'),
        ], string='Partner Type',  default='supplier')
    is_posted = fields.Boolean('Posted Entries Only', default=False)
    category_id = fields.Many2one('res.partner.category', string='Select Category(s)',)

    def print_report(self, data=None):
        data = {'start_date': self.start_date, 'end_date': self.end_date,'category_id': self.category_id.id,'partner_type': self.partner_type,'is_posted': self.is_posted}
        return self.env.ref('de_partner_balance.partner_balance_pdf').report_action(self, data=data)
