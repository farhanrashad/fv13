# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class Car(models.Model):
    _name = 'car'
    _description = 'Car'
    _order = 'id desc'
    
    name = fields.Char('Car', required=True, Help='Car')
    brand_id = fields.Many2one('car.brand', 'Brand', required=True, )
    category_id = fields.Many2one('car.category', 'Category', required=True, )