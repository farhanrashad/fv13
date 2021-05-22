# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    payslip_payment_method = fields.Selection([('cash','By Cash'),('bank','By Bank'),],
                                              string = "Payment", default='cash')
