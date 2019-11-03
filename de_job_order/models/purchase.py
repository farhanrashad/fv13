# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    job_order_id = fields.Many2one('Job.order', string='Job Order Reference', required=False, ondelete='cascade', index=True, copy=False, readonly=True)
                
        