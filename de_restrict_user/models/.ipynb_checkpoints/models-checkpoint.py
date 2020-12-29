# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import exceptions 


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, values):
        t_uid = self.env.uid
        if t_uid == 14 : 
            raise exceptions.ValidationError('you are not allow to create record')
        elif t_uid == 11 : 
            raise exceptions.ValidationError('you are not allow to create record')
        elif t_uid == 19 : 
            raise exceptions.ValidationError('you are not allow to create record')    
        res = super(ResPartner, self).create(values)
        return res
    
    
    @api.multi
    def write(self, values):
        t_uid = self.env.uid
        if t_uid == 14 : 
            raise exceptions.ValidationError('you are not allow to update record')
        elif t_uid == 11 : 
            raise exceptions.ValidationError('you are not allow to update record') 
        elif t_uid == 19 : 
            raise exceptions.ValidationError('you are not allow to update record')    
        res = super(ResPartner, self).write(values)
        return res