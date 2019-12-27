# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class CarRepairRequest(models.Model):
    _name = 'car.repair.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Car Repair'
    _order = 'id desc'
    
    name = fields.Char(string='Order Reference',  copy=False,  index=True, default=lambda self: _('New'))
    title = fields.Char(string='Title',required=True)
    
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    state = fields.Selection([('draft','New'),
                              ('sent','Request Sent'),
                              ('confrim','Repair Order'),
                              ('done','Done'),
                              ('cancel','Cancel')],string = "Status", default='draft',track_visibility='onchange')
    
    partner_id = fields.Many2one('res.partner',string='Customer', required=True, track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    email = fields.Char('Email',related='partner_id.email',readonly=False)
    
    #car information related field
    
    notes = fields.Text(string='Notes')
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('car.repair.request') 
        values['name'] = seq
        res = super(CarRepairRequest,self).create(values)
        return res    