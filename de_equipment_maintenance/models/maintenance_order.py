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
    
    @api.model
    def _get_default_picking_type(self):
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        return self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('warehouse_id.company_id', '=', company_id),
        ], limit=1).id
    
    @api.model
    def _get_default_location_src_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self.env.context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_src_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False

    @api.model
    def _get_default_location_dest_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self._context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_dest_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False
    
    
    
    maintenance_request_id = fields.Many2one('maintenance.request', string="Maintenance Request", help="Related Maintenance Request")
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', required=True,
                                   ondelete='restrict', index=True, check_company=True)
    name = fields.Char(string='Order Reference',  copy=False,  index=True, default=lambda self: _('New'))
    date_order = fields.Date(string='Order Date',required=True, readonly=False, )
    date_confirmed = fields.Date(string='Confirmation Date',required=False, readonly=True, )
    
    schedule_start_date = fields.Date(string='Schedule Start Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    schedule_end_date = fields.Date(string='Schedule End Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    start_date = fields.Date(string='Start Date',required=False, readonly=True, )
    end_date = fields.Date(string='End Date',required=False, readonly=True, )
    
    date_closed = fields.Date(string='Closed Date',required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    user_id = fields.Many2one(
        'res.users', string='Responsible', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="The analytic account related to a sales order.", copy=False, oldname='project_id')
    description = fields.Text(string='Description')
    state = fields.Selection([('draft','New'),
                              ('confirm','Maintenance Order'),
                              ('inprocess','Work in Process'),
                              ('complete','Complete'),
                              ('done','Close'),
                              ('cancel','Cancel')],string = "Status", default='draft',track_visibility='onchange')


    maintenance_part_ids = fields.One2many('maintenance.order.part.lines', 'em_order_id', string='Maintenance Lines', copy=True, auto_join=True)
    
    maintenance_service_ids = fields.One2many('maintenance.order.service.lines', 'em_order_id', string='Maintenance Service Lines', copy=True, auto_join=True)
    
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        domain="[('code', '=', 'internal'), ('company_id', '=', company_id)]",
        default=_get_default_picking_type, required=True, check_company=True)
    location_src_id = fields.Many2one(
        'stock.location', 'Components Location',
        default=_get_default_location_src_id,
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will look for components.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Maintenance Location',
        #default=_get_default_location_dest_id,
        readonly=True, required=True,
        domain="[('usage','=','inventory'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will stock the finished products.")
    
    invoice_method = fields.Selection([
        ("none", "No Invoice"),
        ("b4repair", "Before Repair"),
        ("after_repair", "After Repair")], string="Invoice Method",
        default='none', index=True, readonly=True, required=True,
        states={'draft': [('readonly', False)]},
        help='Selecting \'Before Repair\' or \'After Repair\' will allow you to generate invoice before or after the repair is done respectively. \'No invoice\' means you don\'t want to generate invoice for this repair order.')
    invoice_id = fields.Many2one(
        'account.move', 'Invoice',
        copy=False, readonly=True, tracking=True,
        domain=[('type', '=', 'in_invoice')])
    partner_id = fields.Many2one('res.partner', 'Vendor')
    
    picking_ids = fields.One2many('stock.picking', 'em_order_id', string='Transfers')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    
    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)
            
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_id=picking_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('maintenance.order') 
        values['name'] = seq
        res = super(MaintenanceOrder,self).create(values)
        return res
    
    def action_confirm(self):
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'confirm',
            'date_order': fields.Datetime.now()
        })
    
    def action_start_maintenance(self):
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'inprocess',
            'start_date': fields.Datetime.now()
        })
    
    def action_end_maintenance(self):
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'complete',
            'end_date': fields.Datetime.now()
        })
        
    
    def action_create_delivery(self):
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)
        stock_location = warehouse.lot_stock_id
        vals = {
                'move_type':'one',
                'scheduled_date':fields.Datetime.now(),
                'picking_type_id':self.picking_type_id.id,
                'location_id': self.location_src_id.id,
                'location_dest_id': self.location_dest_id.id,
                'em_order_id': self.id,
            }
        picking_id = self.env['stock.picking'].create(vals)
        for line in self.maintenance_part_ids:
            vals = {
                'company_id':self.company_id.id,
                'name': self.name,
                'date':fields.Datetime.now(),
                'date_expected':fields.Datetime.now(),
                'location_id': self.location_src_id.id,
                'location_dest_id': self.location_dest_id.id,
                'picking_id': picking_id.id,
                'product_id':line.product_id.id,
                'product_uom':line.product_uom_id.id,
                'product_uom_qty': line.product_uom_qty,
                
            }
            move_id = self.env['stock.move'].create(vals)
            
    def action_create_bill(self):
        vals = {
           'test':1, 
        }
        for line in self.maintenance_service_ids:
            vals = {
                'test':1,
            }
    
class MaintenanceParts(models.Model):
    _name = 'maintenance.order.part.lines'
    _description = "Maintenance Part Lines"
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    
    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product',required=True, domain="[('type', 'in', ['product', 'consu'])]" )
    product_uom_qty = fields.Float(string='Quantity', required=True, digits=dp.get_precision('Product Unit of Measure'), default=1.0)
    product_uom_id = fields.Many2one('uom.uom', required=True, string='Unit of Measure',change_default=True, default=_get_default_product_uom_id, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

class MaintenanceOperations(models.Model):
    _name = 'maintenance.order.service.lines'
    _description = "Maintenance Service Lines"
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    
    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product',required=True, domain="[('type', 'not in', ['product', 'consu'])]", )
    product_uom_qty = fields.Float(string='Quantity', required=True, digits=dp.get_precision('Product Unit of Measure'), default=1.0)
    product_uom_id = fields.Many2one('uom.uom', required=True, string='Unit of Measure',change_default=True, default=_get_default_product_uom_id, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    
    
class MaintenanceCost(models.Model):
    _name = 'maintenance.cost'
    _description = "Maintenance Cost"
