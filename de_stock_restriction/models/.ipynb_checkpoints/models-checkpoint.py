# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import exceptions 


class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_locations = fields.Boolean('Restrict Location')

    stock_location_ids = fields.Many2many(
        'stock.location',
        'location_security_stock_location_users',
        'user_id',
        'location_id',
        'Stock Locations')

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type',  string='Default Operations Type')
    

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    @api.model
    def create(self, values):
#         t_uid = self.env.uid
#         if t_uid == 1 : 
        if self.user_has_groups('de_stock_restriction.group_disable_stock_operation'):
            raise exceptions.ValidationError('You are not allowed to create Picking')
        res = super(StockPicking, self).create(values)
        return res
        
    
#     @api.model
#     def create(self, values):
#         t_uid = self.env.uid
#         if t_uid == 1 : 
#             if values['picking_type_id'] == 22 or  values['picking_type_id'] == 23 or  values['picking_type_id'] == 21 or  values['picking_type_id'] == 25 or  values['picking_type_id'] == 26 or values['picking_type_id'] == 30 or values['picking_type_id'] == 29 or values['picking_type_id'] == 31 or values['picking_type_id'] == 151 or values['picking_type_id'] == 155 or values['picking_type_id'] == 152 or values['picking_type_id'] == 156:
#                 raise exceptions.ValidationError('You are not allowed to create Picking')
#         res = super(StockPicking, self).create(values)
#         return res

#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100