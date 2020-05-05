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
    _name = "report.de_sale_stock_report.de_sale_stock_pdf_report"

    
    def _get_report_values(self, docids, data=None):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        query_param = ''
        
        if data['sale_id']:
            query_param = query_param + " and a.state in ('posted') "
        else:
            query_param = query_param + " and a.state in ('draft','posted') "

        cr = self._cr
        query = """
        select a.product_name, a.product_id as product, a.quantity as quantity, a.product_weight as weight, a.location_id as location from
(
select q.product_id, pt.name as product_name, q.location_id, q.lot_id, q.quantity, q.product_weight 
from stock_quant q
join product_product pp on q.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
where a.reconcile = True
and (m.date between %(start_date)s and %(end_date)s)
union all
select q.product_id, pt.name as product_name, q.location_id, q.lot_id, q.quantity, q.product_weight 
from stock_quant q
join product_product pp on q.product_id = pp.id
join product_template pt on pp.product_tmpl_id = pt.id
where a.reconcile = True
and (m.date <= %(start_date)s)
) a where a.product_name != '' """ + query_param + """
group by a.product_name
order by 1
        """ 
        
        params = {'start_date': data['start_date'], 'end_date':data['end_date'],'sale_id':data['sale_id'],}

        self.env.cr.execute(query, params=params)
        
        #cr.execute(query, [data['partner_id'],,])
        dat = cr.dictfetchall()

        return {
            'doc_ids': self.ids,
            'doc_model': 'sale.stock',
            'dat': dat,
            'data': data,
            'docs': docs
        }
