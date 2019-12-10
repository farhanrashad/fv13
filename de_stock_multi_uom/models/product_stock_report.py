# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductStockReport(models.AbstractModel):
    _name = "report.product.stock.pdf"
    _description = "Product Stock Reprot"

    def get_report_values(self,docids,data=None):
        
        query_get_product = ''
        if data['product_id']:
            query_get_product = ' and (a.product_id = ' + str(data['product_id']) + ') '
        else:
            query_get_product = ''
        
                       
        query_get_pricelist = ''
        if data['pricelist_id']:
            query_get_pricelist = ' and (a.pricelist_id = ' + str(data['pricelist_id']) + ') '
        else:
            query_get_pricelist = ''
        
        
        cr = self._cr
        query = """
        select a.product_id, a.default_code, a.barcode, a.product_tmpl_id, a.product_name, a.category_name, a.lot, max(a.list_price) as list_price, sum(a.quantity) as quantity  from (

select  p.default_code, t.categ_id, s.product_id, p.product_tmpl_id, p.barcode, t.name as product_name, g.name as category_name, b.name as lot, l.name as location, t.list_price, s.quantity
from stock_quant s
join product_product p on s.product_id = p.id
join product_template t on p.product_tmpl_id = t.id
join product_category g on t.categ_id = g.id
left join stock_location l on s.location_id = l.id
left join stock_production_lot b on s.lot_id = b.id
where l.usage != 'view'
and s.in_date <= %(dated)s
and l.id = %(location_id)s
        ) a where a.product_id is not null and a.categ_id in %(categ_ids)s """ + query_get_product + """
        group by a.product_name, a.product_id, a.category_name, a.lot, a.product_tmpl_id,a.barcode,a.default_code
        having (sum(a.quantity)) > 0
        order by a.category_name
        """
        params = {
            'dated': data['dated'],
            'warehouse_id': data['warehouse_id'],
			'location_id': data['location_id'],
            'categ_ids': tuple(data['categ_ids']),
        }

        self.env.cr.execute(query, params=params)
        
        dat = cr.dictfetchall()

        return {
            'doc_ids': self.ids,
            'doc_model': 'report.product.stock.wizard',
            'dat': dat,
            'data': data,
        }
    
    