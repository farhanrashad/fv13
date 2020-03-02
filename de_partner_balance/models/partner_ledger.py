# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015 Dynexcel (<http://dynexcel.com/>).
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
    is_vendor = fields.Boolean('Vendor Balances', default=False)
    is_customer = fields.Boolean('Customer Balances', default=False)
    #partner_id = fields.Many2one('res.partner', string='Partner', required=True, help='Select Partner for movement')

    def print_report(self, data):
        data = {'start_date': self.start_date, 'end_date': self.end_date,'is_vendor': self.is_vendor,'is_customer': self.is_customer}
        return self.env.ref('de_partner_balance.partner_balance_pdf').report_action(self, data=data)
