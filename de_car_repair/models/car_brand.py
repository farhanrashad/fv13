# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class CarBrand(models.Model):
    _name = 'car.brand'
    _description = 'Car Brand'
    _order = 'id desc'
    
    name = fields.Char('Brand', required=True, Help='Car Brand/Manufacturer')