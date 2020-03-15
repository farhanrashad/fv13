# -*- coding: utf-8 -*-


import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError

class ReportOrderStock(models.AbstractModel):
    _name = 'report.order.stock.balance'
    _description = 'Order Stock Balance'

    '''Find Outstanding invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        outstanding_invoice = []
        
        moves = self.env['stock.move'].search([])
        if len(moves) > 1:
            return {
                'doc_ids': self.ids,
                'docs': docs,
                'moves': moves,
            }
        else:
            raise UserError("There is not any Stock Mvoes")
            
        return {
                'doc_ids': self.ids,
                'docs': docs,
                'moves': moves,
            }
