# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from odoo.addons import decimal_precision as dp


class JobOrder(models.Model):
    _name = 'job.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Job Order'
    _order = 'date_order desc, id desc'
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    struct_id = fields.Many2one('job.order.structure', string='Structure',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Defines the rules that have to be applied to this Job Order, accordingly ')
    
    sale_id = fields.Many2one('sale.order', 'Order Reference',required=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('processed', 'Processed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    
    note = fields.Text(string="Note")
    
    job_order_lines = fields.One2many('job.order.line', 'job_order_id', string='Job Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    
    job_order_sale_lines = fields.One2many('job.order.sale.line', 'job_order_id', string='Order Sale Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    
    #details_by_component = fields.One2many('hr.payslip.line',compute='_compute_details_by_salary_rule_category', string='Details by Salary Rule Category')
    
    details_by_component_category = fields.One2many('job.order.line', compute='_compute_details_by_component_category', string='Details by Salary Rule Category')
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('job.order') or ' '
        res_id = super(JobOrder, self).create(vals)
        return res_id
    
    def compute_job(self):
        
        self.job_order_lines.unlink()
        self.write({'state':'process'})
        job_order_line = self.env['job.order.line']
        for job in self:
            for sale in job.job_order_sale_lines:
                #sale = sale.id
                for rule in job.struct_id.rule_ids:
                    #rule = rule.id
                    #localdict = dict(sale=sale, rule=rule)
                    #localdict['result'] = None
                    #localdict['result_qty'] = 1.0
                    #localdict['result_rate'] = 100
                    #qty = rule._compute_rule(localdict)
            
                    result_dict = {
                        'job_order_id':job.id,
                        'job_sale_line_id':sale.id,
                        'name':rule.name,
                        'code':rule.code,
                        'sequence':rule.sequence,
                        'category_id':rule.category_id.id,
                        'job_rule_id':rule.id,
                        'line_desc':rule.name,
                        'quantity':sale.product_uom_qty,
                    }
                    job_order_line.create(result_dict)
    
    def generate_sale_lines(self):
        vals = {}
        self.job_order_sale_lines.unlink()
        self.write({'state':'confirm'})
        job_sale_line = self.env['job.order.sale.line']
        for line in self.sale_id.order_line:
            vals = {
                'job_order_id': self.id,
                'product_tmpl_id': line.product_id.product_tmpl_id.id,
                'product_id': line.product_id.id,
                'product_uom_qty' : line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'sale_line_id': line.id,
                'struct_id': self.struct_id.id,
            }
            job_sale_line.create(vals)
            
    def _compute_details_by_component_category(self):
        for job in self:
            job.details_by_component_category = job.mapped('job_order_lines').filtered(lambda line: line.category_id)
    
class JobOrderSaleLine(models.Model):
    _name = 'job.order.sale.line'
    _description = 'Job Order Sale Line'
    _order = 'id desc'
    
    @api.model
    def _get_default_uom(self):
        return self.product_tmpl_id.uom_id
    
    job_order_id = fields.Many2one('Job.order', string='Job Order Reference', required=True, ondelete='cascade', index=True, copy=False, readonly=True)
    
    sale_line_id = fields.Many2one('sale.order.line', string='Order Line', required=True, index=True)
    
    code = fields.Char(required=False,
        help="The code of Job rules can be used as reference in computation of other rules. "
             "In that case, it is case sensitive.")
    
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product',
        domain="[('type', 'in', ['product', 'consu'])]", required=False)
    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        domain="['&', ('product_tmpl_id', '=', product_tmpl_id), ('type', 'in', ['product', 'consu'])]",
        help="If a product variant is defined the BOM is available only for this product.")
    
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',change_default=True, default=_get_default_uom)
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    struct_id = fields.Many2one('job.order.structure', string='Structure', readonly=True)
    
    @api.depends('product_uom_qty')
    def _get_secondary_qty(self):
        """
        Compute the total Quantity Weight of the SO Line.
        """
        for line in self:
            line.secondary_qty = line.product_uom_qty * line.product_id.product_tmpl_id.secondary_unit_qty
            line.secondary_uom = line.product_id.product_tmpl_id.secondary_uom_id.name
    
    
class JobOrderLine(models.Model):
    _name = 'job.order.line'
    _inherit = 'job.order.rule'
    _description = 'Job Order Line'
    _order = 'sequence'
    
    job_order_id = fields.Many2one('Job.order', string='Job Order Reference', required=True, ondelete='cascade', index=True, copy=False, readonly=True)
    job_sale_line_id = fields.Many2one('job.order.sale.line', string='Job Order Sale Line', required=False, index=True)
    
    job_rule_id = fields.Many2one('job.order.rule', 'Job Rule',required=True)
    line_desc = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', required=True, digits=dp.get_precision('Product Unit of Measure'), default=1.0)