# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class CarRepairOrder(models.Model):
    _name = 'car.repair.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Car Repair Order'
    _order = 'id desc'
    
    name = fields.Char(string='Order Reference',  copy=False,  index=True, default=lambda self: _('New'))
    title = fields.Char(string='Title',required=True, readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    request_date = fields.Date(string='Request Date',required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
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
    
    project_id = fields.Many2one("project.project", string="Project", domain="[('allow_timesheets', '=', True), ('company_id', '=', company_id)]")
    task_id = fields.Many2one("project.task", string="Task", domain="[('project_id', '=', project_id), ('company_id', '=', company_id)]", tracking=True, help="The task must have the same customer as this ticket.")
    #timesheet_ids = fields.One2many('account.analytic.line', 'helpdesk_ticket_id', 'Timesheets')
    
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="The analytic account related to a sales order.", copy=False, oldname='project_id')
    
    state = fields.Selection([('draft','New'),
                              ('sent','Request Sent'),
                              ('confirm','Repair Order'),
                              ('inprocess','Work in Process'),
                              ('repaired','Repaired'),
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
    car_id = fields.Many2one('car', 'Car', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Car", copy=False)
    category_id = fields.Many2one(related='car_id.category_id', readonly=True, string='Category', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    brand_id = fields.Many2one(related='car_id.brand_id', readonly=True, string='Brand', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    model = fields.Char(string='Car Model', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    color = fields.Char(string='Color', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    year = fields.Char(string='Year', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    
    
    description = fields.Text(string='Description')
    
    order_service_lines = fields.One2many('car.repair.order.service', 'car_repair_order_id', string='Car Repair Order Services', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True, auto_join=True)
    invoice_count = fields.Integer(compute="_compute_invoice", string='Invoice Count', copy=False, default=0, store=True)
    order_lines = fields.One2many('car.repair.order.line', 'car_repair_order_id', string='Car Repair Order Lines', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True, auto_join=True)
    invoice_ids = fields.Many2many('account.move', compute="_compute_invoice", string='Bills', copy=False, store=True)
    invoice_status = fields.Selection([
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'Fully Billed'),
    ], string='Invoice Status', compute='_get_invoiced', store=True, readonly=True, copy=False, default='no')
    
    
    @api.depends('order_lines.invoice_lines.move_id')
    def _compute_invoice(self):
        for order in self:
            invoices = order.mapped('order_lines.invoice_lines.move_id')
            order.invoice_ids = invoices
            order.invoice_count = len(invoices)
            
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('car.repair.order') 
        values['name'] = seq
        res = super(CarRepairOrder,self).create(values)
        return res
    
    def action_confirm(self):
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'confirm',
            'date_order': fields.Datetime.now()
        })
    
    def action_start_repair(self):
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'inprocess',
            'start_date': fields.Datetime.now()
        })
    
    def action_end_repair(self):
        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'repaired',
            'end_date': fields.Datetime.now()
        })
    
    def action_quotation_send(self):
        self.write({
            'state': 'sent',
        })
    
    def action_view_invoice(self):
        '''
        This function returns an action that display existing vendor bills of given purchase order ids.
        When only one found, show the vendor bill immediately.
        '''
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        create_invoice = self.env.context.get('create_invoice', False)
        # override the context to get rid of the default filtering
        result['context'] = {
            'default_type': 'out_invoice',
            'default_company_id': self.company_id.id,
            'default_sale_id': self.id,
        }
        # choose the view_mode accordingly
        if len(self.invoice_ids) > 1 and not create_invoice:
            result['domain'] = "[('id', 'in', " + str(self.invoice_ids.ids) + ")]"
        else:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                result['views'] = form_view
            # Do not set an invoice_id if we want to create a new bill.
            if not create_invoice:
                result['res_id'] = self.invoice_ids.id or False
        result['context']['default_origin'] = self.name
        #result['context']['default_reference'] = self.partner_ref
        return result
    
    @api.depends('state', 'order_lines.product_uom_qty')
    def _get_invoiced(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for order in self:
            if order.state not in ('confirm', 'done'):
                order.invoice_status = 'no'
                continue

            if any(float_compare(line.qty_invoiced, line.product_qty if line.product_id.purchase_method == 'purchase' else line.qty_received, precision_digits=precision) == -1 for line in order.order_lines):
                order.invoice_status = 'to invoice'
            elif all(float_compare(line.qty_invoiced, line.product_qty if line.product_id.purchase_method == 'purchase' else line.qty_received, precision_digits=precision) >= 0 for line in order.order_lines) and order.invoice_ids:
                order.invoice_status = 'invoiced'
            else:
                order.invoice_status = 'no'
        
class CarRepairOrderService(models.Model):
    _name = 'car.repair.order.service'
    _description = 'Car Repair Order Service'
    _order = 'id desc'
    
    car_repair_order_id = fields.Many2one('car.repair.order', string='Car Repair Order', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', domain="[('type', 'not in', ['product', 'consu'])]", required=True,)
    product_uom_qty = fields.Float('Quantity', default=1.0, required=True)
    
    
class CarRepairOrderline(models.Model):
    _name = 'car.repair.order.line'
    _description = 'Car Repair Order Line'
    _order = 'id desc'
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    
    car_repair_order_id = fields.Many2one('car.repair.order', string='Car Repair Order', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', domain="[('type', 'in', ['product', 'consu']),('is_spare_part', '=', True)]", required=True,)
    product_uom_qty = fields.Float('Quantity', default=1.0, required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_product_uom_id, required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control", domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    invoice_lines = fields.One2many('account.move.line', 'car_repair_line_id', string="Bill Lines", readonly=True, copy=False)