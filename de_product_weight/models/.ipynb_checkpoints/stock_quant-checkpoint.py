# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    product_weight = fields.Float('Total Weight')    
    