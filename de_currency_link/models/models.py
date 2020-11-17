# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
from datetime import datetime
from openerp.exceptions import Warning, ValidationError


class Codec(models.Model):
    _inherit = 'res.currency'
    _description = 'MultiCurrency From Official Website Of State Bank Of MYANMAR'

    def schedular_fun(self):
        try:
            scheduler = self.env['ir.cron'].search([('name', '=', 'Currency Scheduler')])
            if not scheduler:
                scheduler = self.env['ir.cron'].search([('name', '=', 'Currency Scheduler'),
                                                        ('active', '=', False)])
            scheduler.active = True
            scheduler.interval_number = 1
            scheduler.interval_type = 'work_days'
            scheduler.nextcall = datetime()

        except Exception as e:
            raise ValidationError(str(e))

    def currency_check(self):

        url = "http://forex.cbm.gov.mm/api/latest"

        payload = {}
        files = {}
        headers = {
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        json_responce = response.json()['rates']

        currency_get = self.env.company.currency_id
        print('debug')

        try:
            # converion_api = float(json_responce['USD'])
            converion_api = float(json_responce[currency_get.name])

        except Exception:
            # converion_api = float(json_responce['USD'].split(',')[0] + json_responce['USD'].split(',')[1])
            converion_api = float(json_responce[currency_get.name].split(',')[0] + json_responce[currency_get.name].split(',')[1])

        # euro_search_odoo = self.env['res.currency'].search([('name', '=', 'USD')])[0]
        euro_search_odoo = self.env['res.currency'].search([('name', '=', currency_get.name)])[0]

        if not euro_search_odoo:
            pass
        else:
            today_currency_check = self.env['res.currency.rate'].search([('name', '=', datetime.now().date()), ('currency_id', '=', euro_search_odoo.id)])
            if not today_currency_check:
                self.env['res.currency.rate'].create({
                    'currency_id': euro_search_odoo.id,
                    'rate': converion_api,
                    'name': datetime.now().date()
                })
            else:
                self.env['res.currency.rate'].write({
                    'currency_id': euro_search_odoo.id,
                    'rate': converion_api,
                    'name': datetime.now().date()
                })


