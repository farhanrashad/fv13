# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################

import time

from odoo import fields,api,models
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class ProductLedger(models.TransientModel):

    _name = 'product.ledger'
    
    start_date = fields.Datetime(required=True, default=fields.datetime.today().replace(day=1))
    end_date = fields.Datetime(required=True, default=fields.Datetime.now)

    product_id = fields.Many2one('product.product', string='Product', required=True, help='Select Product for movement')
    location_id = fields.Many2one('stock.location', string='Location', help='Enter the location to filter records')
    
    def print_report(self, data):
        data = {'product_id': self.product_id.id,'start_date': self.start_date, 'end_date': self.end_date,'location_id':self.location_id.id}
        return self.env.ref('de_product_ledger.product_ledger_pdf').report_action(self, data=data)
    
    def _print_report(self, data):
        data = self.pre_print_report(data)
        data = {'product_id': self.product_id.id,'start_date': self.start_date, 'end_date': self.end_date,'location_id':self.location_id.id}
        
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('de_product_ledger.product_ledger_pdf').with_context(landscape=True).report_action(records, data=data)

