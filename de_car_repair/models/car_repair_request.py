# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class CarRepairRequest(models.Model):
    _name = 'car.repair.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Car Repair Order'
    _order = 'id desc'
    
    name = fields.Char(string='Order Reference',  copy=False,  index=True, default=lambda self: _('New'))
    title = fields.Char(string='Title',required=True, readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    request_date = fields.Date(string='Request Date',required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    start_date = fields.Date(string='Start Date',required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    end_date = fields.Date(string='End Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    date_closed = fields.Date(string='Closed Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    
    project_id = fields.Many2one("project.project", string="Project", domain="[('allow_timesheets', '=', True), ('company_id', '=', company_id)]")
    task_id = fields.Many2one("project.task", string="Task", domain="[('project_id', '=', project_id), ('company_id', '=', company_id)]", tracking=True, help="The task must have the same customer as this ticket.")
    #timesheet_ids = fields.One2many('account.analytic.line', 'helpdesk_ticket_id', 'Timesheets')
    
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="The analytic account related to a sales order.", copy=False, oldname='project_id')
    
    state = fields.Selection([('draft','New'),
                              ('sent','Request Sent'),
                              ('confirm','Repair Order'),
                              ('inprocess','Work in Process'),
                              ('done','Done'),
                              ('cancel','Cancel')],string = "Status", default='draft',track_visibility='onchange')
    
    partner_id = fields.Many2one('res.partner',string='Customer', required=True, track_visibility='onchange', readonly=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    phone = fields.Char('Phone',related='partner_id.phone',readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    mobile = fields.Char('Mobile',related='partner_id.mobile',readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    email = fields.Char('Email',related='partner_id.email',readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    street = fields.Char('Street',related='partner_id.street',readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    street2 = fields.Char('Street2',related='partner_id.street2',readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    city = fields.Char('City',related='partner_id.city',readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    #car information related field
    
    notes = fields.Text(string='Notes')
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('car.repair.order') 
        values['name'] = seq
        res = super(CarRepairRequest,self).create(values)
        return res    