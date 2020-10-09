# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class MRPProduction(models.Model):
    _inherit = 'mrp.production'
    
    global_ref = fields.Char(related='job_order_id.sale_id.global_ref', string='Global Reference', store=True)