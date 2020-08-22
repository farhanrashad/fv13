# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ReportData(models.AbstractModel):
    _name = 'report.de_custom_proforma_invoice.custom_proforma_invoice1'
    _description = 'Report Data'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        register_ids = self.env.context.get('active_ids', [])
        contrib_registers = self.env['sale.order'].browse(register_ids)
        date_from = data['form'].get('date', fields.Date.today())
        date_to = data['form'].get('date', str(datetime.now() + relativedelta(months=+1, day=1, days=-1))[:10])
        # lines_data = self._get_payslip_lines(register_ids, date_from, date_to)
        # lines_total = {}
        # for register in contrib_registers:
        #     lines = lines_data.get(register.id)
        #     lines_total[register.id] = lines and sum(lines.mapped('total')) or 0.0
        print('11111111')
        return {
            'doc_ids': register_ids,
            'doc_model': 'sale.order',
            'docs': contrib_registers,
            'data': data,
            # 'lines_data': lines_data,
            # 'lines_total': lines_total
        }
