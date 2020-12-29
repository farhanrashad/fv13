# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        taxes_grouped = self.get_taxes_values()
        tax_lines = self.tax_line_ids.filtered('manual')
        for tax in taxes_grouped.values():
            tax_lines += tax_lines.new(tax)
        self.tax_line_ids = tax_lines
        return