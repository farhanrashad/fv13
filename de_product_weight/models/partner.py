# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_purchase_weight = fields.Boolean("Compute prices in weight", default=False)