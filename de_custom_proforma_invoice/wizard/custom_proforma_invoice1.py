# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CustomProformaInvoice(models.TransientModel):
    _name = 'custom.proforma.invoice'

    def action_print_custom_proforma_invoice1(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'sale.order',
            'form': self.read()[0]
        }
        print('k-->', datas)
        return self.env.ref('de_custom_proforma_invoice.report_custom_proforma1_pdf').report_action([], data=datas)

    name = fields.Char(string='Name')
    proforma_invoice_no = fields.Many2one(comodel_name='sale.order', string='Proforma Invoice')
    date = fields.Date(string='Date')
    order_id = fields.Char(string='Order No')
    fca_price_total = fields.Float(string='Total FCA Sialkot Price')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    income_term = fields.Char(string='Income Term')
    latest_shipment_date = fields.Date(string='Latest Shipment Date')
    payment_term = fields.Char(string='Payment Term')
    shipment_by = fields.Char(string='Shipment By')
    partial_shipment = fields.Char(string='Partial Shipment')
    shipment = fields.Char(string='TranShipment')
    bank_id = fields.Many2one(comodel_name='account.journal', string='Bank')
    lot_no = fields.Char(string='LOT No')
    prs_no = fields.Char(string='PRS')
