# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class ProductStockReport(models.TransientModel):
    _name = "report.product.stock.wizard"
    _description = "Product Stock Report"
    
    dated = fields.Datetime(required=True, default=fields.Datetime.now)
    
    product_id = fields.Many2one('product.product', string='Product', required=False, help='Select Product for movement')
    categ_ids = fields.Many2many('product.category', string='Categories')
    


    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update(self.read(['dated', 'product_id','categ_ids'])[0])
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('de_stock_multi_uom.action_report_product_stock').with_context(landscape=True).report_action(records, data=data)
