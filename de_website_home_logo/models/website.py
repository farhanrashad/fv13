# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Website(models.Model):
    _inherit = 'website'
    
    home_logo = fields.Binary('Website Homepage Logo', help="Display this homepage logo on the website.")
