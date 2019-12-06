# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    product_weight = fields.Float('Total Weight')