# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date

class MoBeforhandWizard(models.TransientModel):
    _name = 'mrp.mo.beforehand.wizard'
    _description = 'Select Vendor for order line'
    
    
    partner_id = fields.Many2one('res.partner', string="Vendor")
    
    
#     def amend_entries(self):
        
