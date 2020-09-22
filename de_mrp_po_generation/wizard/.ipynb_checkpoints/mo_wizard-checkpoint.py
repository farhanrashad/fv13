# -*- coding: utf-8 -*-

from . import models

class MoBeforhandWizard(models.Model):
    _name = 'mrp.mo.beforehand.wizard'
    _description = 'Select Vendor for order line'
    
    
    partner_id = fields.Many2one('purchase.order', string="Vendor")
