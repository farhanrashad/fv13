# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleCustomProformaInvoice(models.Model):
    _inherit = 'sale.order'

    def custom_proforma_invoice1_button(self):
        wizard_view_id = self.env.ref(
            'de_custom_proforma_invoice.custom_proforma_invoice1_wizard')
        return {
            'name': _('Proforma Invoice'),
            'res_model': 'custom.proforma.invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': wizard_view_id.id,
            'target': 'new',
        }
