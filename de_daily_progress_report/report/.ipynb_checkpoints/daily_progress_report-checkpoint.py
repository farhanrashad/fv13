# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#################################################################################

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError

class DailyProgressReport(models.AbstractModel):
    _name = 'report.de_daily_progress_report.progress_report_template'

    '''Find Purchase invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self, docids, data=None):       
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        outstanding_invoice = []       
        
        lot_records = self.env['stock.move.line'].search([('date', '=', docs.date),
                                                          ])


        if lot_records:
             return {
                'docs': docs,
                 'lot_records': lot_records,
             }
        else:
            raise UserError("There is not any Record between selected date")

            
    
