# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HRPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    state = fields.Selection(selection_add=[('paid', 'Paid')],string='Status', readonly=True, copy=False, default='draft')