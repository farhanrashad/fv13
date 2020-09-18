# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
   
    style = fields.Char(srting='Stle', store=True)
    color = fields.Char(string='Color', store=True)
    hs_code = fields.Char(string='H.S Code', store=True)
    composition = fields.Char(string='Composition', store=True)
    