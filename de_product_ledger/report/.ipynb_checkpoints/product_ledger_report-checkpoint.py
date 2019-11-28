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
    _name = "report.de_product_ledger.de_product_ledger_pdf_report"

    def _get_report_values(self,docids,data=None):
        query_get_location = ''
        if data['location_id']:
            query_get_location = ' and (ml.location_id = ' + str(data['location_id']) + ' or ml.location_dest_id = ' + str(data['location_id']) + ')'
        else:
            query_get_location = ''
        cr = self._cr
        query = """select sum(case 
        when loc1.usage = 'internal' and loc2.usage != 'internal' then ml.qty_done * -1 
        when loc2.usage = 'internal' and loc1.usage != 'internal' then ml.qty_done
        else 0
        end) as open_stk
        from stock_move_line ml
        left join stock_move m on ml.picking_id = m.id
        join product_product p on ml.product_id = p.id
        join product_template t on p.product_tmpl_id = t.id
        left join stock_production_lot l on ml.lot_id = l.id
        join stock_location loc1 on ml.location_id = loc1.id
        join stock_location loc2 on ml.location_dest_id = loc2.id
        where loc1.usage != 'view' and loc2.usage != 'view'
        and ml.product_id = %s and ml.date < %s
        """ + query_get_location
        cr.execute(query, [data['product_id'],data['start_date']])
        openstk = cr.dictfetchall()

        cr = self._cr
        query = """select ml.date, ml.reference, p.default_code, t.name as product_name, l.name as lot, loc1.complete_name as source, loc1.usage as source_usage,
        loc2.complete_name as destination, loc2.usage as dest_usage,
        ml.qty_done,
        (case
        when loc2.usage = 'internal' and loc1.usage != 'internal' then ml.qty_done
        else 0
        end) as in_qty,
         (case
        when loc1.usage = 'internal' and loc2.usage != 'internal' then ml.qty_done 
        else 0
        end) as out_qty
        from stock_move_line ml
        left join stock_move m on ml.picking_id = m.id
        join product_product p on ml.product_id = p.id
        join product_template t on p.product_tmpl_id = t.id
        left join stock_production_lot l on ml.lot_id = l.id
        join stock_location loc1 on ml.location_id = loc1.id
        join stock_location loc2 on ml.location_dest_id = loc2.id
        where loc1.usage != 'view' and loc2.usage != 'view'  
        and ml.product_id = %s and (ml.date between %s and %s)
        """ + query_get_location + ' order by ml.date'
        cr.execute(query, [data['product_id'],data['start_date'],data['end_date']])
        dat = cr.dictfetchall()

        return {
            'doc_ids': self.ids,
            'doc_model': 'product.ledger',
            'openstk': openstk,
            'dat': dat,
            'data': data,
        }
