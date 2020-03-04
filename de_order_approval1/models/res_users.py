# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    sale_order_can_approve = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Can Approve Sale?',default='no')
    sale_order_amount_limit = fields.Float("(SO) Amount Limit", digits=(16, 0), required=True)
    sale_order_discount_limit = fields.Float("(SO) Discount Limit", digits=(16, 0), required=True)