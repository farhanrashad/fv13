# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    is_sale_weight = fields.Boolean(related='partner_id.is_sale_weight',string='Enable Weight Pricing',readonly=True)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=True, store=True)
    total_weight = fields.Float(string='Total Weight',default=1.0, digits='Product Unit of Measure',)
    price_weight = fields.Float(string='Price Weight', digits='Product Price')
    
    price_qty_weight = fields.Float(string='Price Qty/Weight', store=False, digits='Product Price',compute='_compute_price_weight')
    
    def _compute_price_weight(self):
        for line in self:
            if line.quantity > 0:
                line.price_qty_weight = (line.total_weight * line.price_weight) / line.quantity
    
