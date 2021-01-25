
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re

class PurchaseOrderInh(models.Model):
    _inherit= 'purchase.order'
    
    def print_po_matrix_report(self):
        data = {}
        data['form'] = self.read(['id','state'])[0]
        return self.env.ref('de_po_matrix_report.action_po_matrix_report').report_action(self, data=data, config=False)

    
class POMatrixReport(models.AbstractModel):
    _name = 'report.de_po_matrix_report.po_matrix_report_templet'
    
    def get_matched_record(self, color, model):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        records_list = []
        for record in docs.order_line:
            data = record.product_id.name
            x = re.search(model, data)
            y = re.search(color, data)
            if x and y:
                records_list.append(record.id)
        rec = self.env['purchase.order.line'].browse(records_list)
        return rec
        
    
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        colors = ''
        description = ''
        color_list = []
        model_list = []
        for record in docs.order_line:
            data = record.product_id.name
            color_name = data.split('(', 1)[1].split(')')[0]
            model_name = data.split('(', 1)[0]
            color_list.append(color_name)
            model_list.append(model_name)
#             raise UserError((colors))
#             raise UserError((description))
#             color = colors.find("(")+1:colors.find(")")

        model_list = list(dict.fromkeys(model_list))

        return {
                'docs': docs,
#                 'orders': invoices,
                'model_list':model_list,
                'color_list': color_list,
                'product_qty': self.get_matched_record,
            }
        
            