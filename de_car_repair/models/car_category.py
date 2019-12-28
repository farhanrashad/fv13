# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class CarCategory(models.Model):
    _name = 'car.category'
    _description = 'Car Category'
    _order = 'id desc'
    
    name = fields.Char('Category', required=True, Help='Car Category')