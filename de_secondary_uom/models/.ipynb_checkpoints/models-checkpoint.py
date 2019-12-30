# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    sec_uom_id = fields.Many2one('uom.uom', string='Sec. UOM')
    sec_qty_factor = fields.Float(string='Factor')