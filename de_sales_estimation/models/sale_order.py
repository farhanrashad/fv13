from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp



class SaleOrderInhert(models.Model):
    _inherit = 'sale.order'


    estimate_id = fields.Many2one(comodel_name="sale.estimate", string="Estimate", required=False, )
    origin_id = fields.Char(string="Estimate", required=False, )

    qute_count_id = fields.Integer(compute='_compute_estimate_data_id', string="Number of Estimations")
    quote_ids = fields.One2many('sale.estimate', 'quote_id', string='Orders')

    # @api.depends('estimate_ids.state',  'order_ids.amount_untaxed', 'order_ids.date_order', 'order_ids.company_id')
    def _compute_estimate_data_id(self):
        for lead in self:
            total = 0.0
            estimation_quo = 0
            qute_count_id = 0
            quotation_cnt = 0

            for order in lead.quote_ids:
                if order.state in ('draft', 'sent'):
                    quotation_cnt += 1
                lead.qute_count_id = quotation_cnt


