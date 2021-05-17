# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import exceptions 


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, values):
        t_uid = self.env.uid
        if t_uid == 54 : 
            raise exceptions.ValidationError('You are not allowed to create customers / vendors') 
        res = super(ResPartner, self).create(values)
        return res
    
    
    @api.multi
    def write(self, values):
        t_uid = self.env.uid
        if t_uid == 54 : 
            raise exceptions.ValidationError('You are not allowed to update customers / vendors')
        res = super(ResPartner, self).write(values)
        return res

    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, values):
        t_uid = self.env.uid
        if t_uid == 54 : 
            raise exceptions.ValidationError('You are not allowed to create Purchase Order') 
        res = super(PurchaseOrder, self).create(values)
        return res
    
    
    @api.multi
    def write(self, values):
        t_uid = self.env.uid
        if t_uid == 54 : 
            raise exceptions.ValidationError('You are not allowed to update Purchase Order')
        res = super(PurchaseOrder, self).write(values)
        return res    

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, values):
        t_uid = self.env.uid
        if t_uid == 54 : 
            raise exceptions.ValidationError('You are not allowed to create Sale Order') 
        res = super(SaleOrder, self).create(values)
        return res
    
    
    @api.multi
    def write(self, values):
        t_uid = self.env.uid
        if t_uid == 54 : 
            raise exceptions.ValidationError('You are not allowed to update Sale Order')
        res = super(SaleOrder, self).write(values)
        return res        