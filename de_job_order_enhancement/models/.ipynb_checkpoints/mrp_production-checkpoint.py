# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp
import threading




class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    production_total_weight = fields.Float(string='Production Weight')

    

