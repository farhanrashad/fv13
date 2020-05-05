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

    _name = 'sale.stock'

    start_date = fields.Date(
        string='From Date',
        required=True
    )
    end_date = fields.Date(
        string='To Date',
        required=True
    )
    location_id = fields.Many2one('stock.location', string='Select Location',)

    def print_report(self, data=None):
        data = {'start_date': self.start_date, 'end_date': self.end_date,'location_id': self.location_id.id}
        return self.env.ref('de_sale_stock_report.sale_stock_pdf').report_action(self, data=data)
