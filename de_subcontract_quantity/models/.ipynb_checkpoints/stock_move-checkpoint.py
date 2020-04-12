# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    subcontract_order_line_id = fields.Many2one('purchase.order.line', 'Subcontract Order Line', domain="['|', ('order_id.job_order_id', '=', ref_job_order_id), ('order_id.job_order_id', '=', job_order_id) ]")
