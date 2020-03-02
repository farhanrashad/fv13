# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015 Dynexcel (<http://dynexcel.com/>).
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

    def get_report_values(self,docids,data=None):
        
        query_partner_type = ''
        
        if data['is_vendor']:
            query_partner_type = query_partner_type + ' or x.supplier = True '
        
        if data['is_customer']:
            query_partner_type = query_partner_type + ' or x.customer = True '
        
            

        cr = self._cr
        query = """
        select x.city, x.partner_name, sum(x.obal) as obal, sum(x.debit) as debit, sum(x.credit) as credit, sum(x.obal)+sum(x.debit)+sum(x.credit) as cbal from
        (
        select p.city, p.name as partner_name, p.supplier, p.customer, 0 as obal, l.debit, l.credit
from account_move_line l
join account_move m on l.move_id = m.id
join res_partner p on l.partner_id = p.id
join account_account a on l.account_id = a.id
join account_journal j on m.journal_id = j.id
where a.reconcile = True
        and (m.date between %(start_date)s and %(end_date)s)
        union all
select p.city, p.name as partner_name, p.supplier, p.customer, (l.debit - l.credit) as obal, 0 as debit, 0 as credit
from account_move_line l
join account_move m on l.move_id = m.id
join res_partner p on l.partner_id = p.id
join account_account a on l.account_id = a.id
join account_journal j on m.journal_id = j.id
where a.reconcile = True
        and (m.date <= %(start_date)s)
) x where x.partner_name != '' """ + query_partner_type + """
group by x.city, x.partner_name
order by 1
        """ 
        
        params = {
            'start_date': data['start_date'],
			'end_date':data['end_date'],
        }

        self.env.cr.execute(query, params=params)
        
        #cr.execute(query, [data['partner_id'],,])
        dat = cr.dictfetchall()

        return {
            'doc_ids': self.ids,
            'doc_model': 'partner.balance',
            'dat': dat,
            'data': data,
        }
