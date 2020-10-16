# -*- coding: utf-8 -*-
import xlwt
import base64
from io import StringIO
from odoo import api, fields, models, _
import platform
import time
from dateutil import relativedelta
import dateutil.relativedelta
import datetime
from datetime import date
from datetime import datetime , timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class HelpdeskWizard(models.Model):
    _name = "helpdesk.wizard"
    _description = "Helpdesk Wizard"
    
    
    date_from = fields.Date('Date From:',default=time.strftime('%Y-%m-01'))
    date_to = fields.Date('Date To:',default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],)
    
    stage = fields.Many2one('helpdesk.ticket.stage', string="Stage")


    def action_report_gen(self):
        datas = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'stage': self.stage,
        }
        return self.env.ref('de_helpdesk_ticket_detail_report.emp_att_xlsx').report_action(self,data=datas)