# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    maintenance_count = fields.Integer('Maintenance Count', compute='_compute_maintenance_count', compute_sudo=True)
    maintenance_order_ids = fields.One2many('maintenance.order', 'maintenance_request_id', string='Maintenance Order')
    
    @api.depends('maintenance_order_ids')
    def _compute_maintenance_count(self):
        for order in self:
            order.maintenance_count = len(order.maintenance_order_ids)
            
        #maintenance_data = self.env['maintenance.order'].sudo().read_group([('maintenance_request_id', 'in', self.ids)], ['maintenance_request_id'], ['maintenance_request_id'])
        #mapped_data = dict([(r['maintenance_request_id'][0], r['maintenance_request_id_count']) for r in maintenance_data])
        #for mr in self:
            #mr.maintenance_count = mapped_data.get(mr.id, 0)

    def action_view_maintenance1(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('maintenance'),
            'res_model': 'maintenance.order',
            'view_mode': 'tree,form',
            'domain': [('maintenance_request_id', '=', self.id)],
            'context': dict(self._context, create=False, default_maintenance_request_id=self.id),
        }
    

class MaintenanceOrder(models.Model):
    _name = 'maintenance.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance Order'
    _order = 'id desc'
    
    maintenance_request_id = fields.Many2one('maintenance.request', string="Maintenance Request", help="Related Maintenance Request")
    
    name = fields.Char(string='Order Reference',  copy=False,  index=True, default=lambda self: _('New'))
    date_order = fields.Date(string='Confirmation Date',required=False, readonly=True, )
    schedule_start_date = fields.Date(string='Schedule Start Date',required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    schedule_end_date = fields.Date(string='Schedule End Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    start_date = fields.Date(string='Start Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    end_date = fields.Date(string='End Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    date_closed = fields.Date(string='Closed Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="The analytic account related to a sales order.", copy=False, oldname='project_id')
    description = fields.Text(string='Description')
    state = fields.Selection([('draft','New'),
                              ('confirm','Repair Order'),
                              ('inprocess','Work in Process'),
                              ('repaired','Repaired'),
                              ('done','Done'),
                              ('cancel','Cancel')],string = "Status", default='draft',track_visibility='onchange')


    maintenance_part_ids = fields.One2many('maintenance.order.part.lines', 'em_order_id', string='Maintenance Lines', copy=True, auto_join=True)
    
    maintenance_service_ids = fields.One2many('maintenance.order.service.lines', 'em_order_id', string='Maintenance Service Lines', copy=True, auto_join=True)
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('maintenance.order') 
        values['name'] = seq
        res = super(MaintenanceOrder,self).create(values)
        return res
    
class MaintenanceParts(models.Model):
    _name = 'maintenance.order.part.lines'
    _description = "Maintenance Part Lines"
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    
    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product',required=True, domain="[('type', 'in', ['product', 'consu'])]" )
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure',change_default=True, default=_get_default_product_uom_id, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

class MaintenanceOperations(models.Model):
    _name = 'maintenance.order.service.lines'
    _description = "Maintenance Service Lines"
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    
    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product',required=True, domain="[('type', 'not in', ['product', 'consu'])]", )
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure',change_default=True, default=_get_default_product_uom_id, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    
    
class MaintenanceCost(models.Model):
    _name = 'maintenance.cost'
    _description = "Maintenance Cost"
