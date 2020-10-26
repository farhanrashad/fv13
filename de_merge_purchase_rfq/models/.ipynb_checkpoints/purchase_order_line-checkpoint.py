# -*- coding: utf-8 -*-

from odoo import api,fields,models,_

class PurchaseOrderLine(models.Model):
    _inherit ='purchase.order.line'  
   
    merge = fields.Boolean(string='Merge')
    

	

