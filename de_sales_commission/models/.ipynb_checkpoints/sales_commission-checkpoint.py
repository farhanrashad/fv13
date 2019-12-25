# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class SalesCommission(models.Model):
    _name = 'sale.commission'
    _description = "Sale Commission"

    agent_id = fields.Many2one('res.partner', string='Agent', required=False, help="Commission Agent")
    doc_date = fields.Datetime(string='Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    commission_amount = fields.Float(string='Commission Amount')
    sale_id = fields.Many2one('sale.order', 'Order Reference',required=False,  readonly=True, )
    is_invoiced = fields.Boolean('Is Invoiced', default=False)
    invoice_id = fields.Many2one('account.move', 'Invoice',required=False,  readonly=True, )
    date_invoiced = fields.Datetime(string='Date Invoiced', required=False, readonly=True)
    