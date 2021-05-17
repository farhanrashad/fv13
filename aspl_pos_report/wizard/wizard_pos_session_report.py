# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields, models, api, _
from odoo.exceptions import Warning

class wizard_pos_session_report(models.TransientModel):
    _name = 'wizard.pos.session.report'

    @api.model
    def get_ip(self):
        proxy_ip = self.env['res.users'].browse([self._uid]).company_id.report_ip_address or''
        return proxy_ip

    @api.multi
    def print_receipt(self):
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'wizard.pos.session.report'
                }
        return self.env.ref('aspl_pos_report.report_pos_session_pdf').report_action(self, data=datas)

    session_ids = fields.Many2many('pos.session', string="Closed Session(s)")
    report_type = fields.Selection([('thermal', 'Thermal'),
                                    ('pdf', 'PDF')], default='pdf', readonly=True, string="Report Type")
    proxy_ip = fields.Char(string="Proxy IP", default=get_ip)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: