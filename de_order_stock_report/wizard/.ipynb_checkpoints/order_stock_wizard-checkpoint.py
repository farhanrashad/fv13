from odoo import api, fields, models, _

class OrderStockWizard(models.TransientModel):
    _name = "report.order.stock.wizard"
    _description = "Stock Production Wizard"

    start_date = fields.Date(string='From Date', required=False, help='select start date')
    end_date = fields.Date(string='To Date', required=False, help='select end date')
    sale_id = fields.Many2one('sale.order', 'Order Reference',required=False, )

    def check_report(self):
        data = {}
        data['form'] = self.read(['start_date', 'end_date','sale_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['start_date', 'end_date','sale_id'])[0])
        return self.env.ref('de_order_stock_report.action_order_stock_report').report_action(self, data=data, config=False)