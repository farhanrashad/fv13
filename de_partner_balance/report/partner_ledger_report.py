# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################
import pytz
import time

from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime


class CustomReport(models.AbstractModel):
    _name = "report.de_partner_balance.de_partner_balance_pdf_report"

    
    def _get_report_values(self, docids, data=None):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        query_partner_type = ''
        
        if data['is_vendor']:
            query_partner_type = query_partner_type + ' or a.supplier_rank = 1 '
        
        if data['is_customer']:
            query_partner_type = query_partner_type + ' or a.customer_rank = 1 '

        if data['category_id']:
            query_partner_type = query_partner_type + ' or a.partner_id in (select partner_id from res_partner_res_partner_category_rel where category_id = ' + data['category_id'] + ') '

        cr = self._cr
        query = """
        select a.partner_name, sum(a.obal) as obal, sum(a.debit) as debit, sum(a.credit) as credit, sum(a.obal)+sum(a.debit-a.credit) as cbal from
(
select p.name as partner_name, p.category_id ,l.partner_id, 0 as obal, l.debit, l.credit
from account_move m
join account_move_line l on l.move_id = m.id
join res_partner p on l.partner_id = p.id
join account_account a on l.account_id = a.id
join account_journal j on m.journal_id = j.id
where a.reconcile = True
and (m.date between %(start_date)s and %(end_date)s)
union all
select p.name as partner_name, p.category_id ,l.partner_id, l.debit - l.credit as obal, 0 as debit, 0 as credit
from account_move m
join account_move_line l on l.move_id = m.id
join res_partner p on l.partner_id = p.id
join account_account a on l.account_id = a.id
join account_journal j on m.journal_id = j.id
where a.reconcile = True
and (m.date <= %(start_date)s)
) a where a.partner_name != '' """ + query_partner_type + """
group by a.partner_name
order by 1
        """ 
        
        params = {'start_date': data['start_date'], 'end_date':data['end_date'],'category_id':data['category_id'],}

        self.env.cr.execute(query, params=params)
        
        #cr.execute(query, [data['partner_id'],,])
        dat = cr.dictfetchall()

        return {
            'doc_ids': self.ids,
            'doc_model': 'partner.balance',
            'dat': dat,
            'data': data,
            'docs': docs
        }
