# -*- coding: utf-8 -*-
from datetime import date
import time
from odoo import models, fields, api, _


class StockwarehouseTransfer(models.Model):
    _name = 'stock.transit.transfer'
    _description = 'This model is use in Stock Tansfer'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    
    name = fields.Char(string='Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    source_warehouse_id = fields.Many2one(
        'stock.warehouse', 'Source Warehouse', ondelete='cascade',
        check_company=True, states={'draft': [('readonly', False)]})
    location_id = fields.Many2one(
        'stock.location', "Transit Location",
        check_company=True,  required=True,
        states={'draft': [('readonly', False)]})

    dest_warehouse_id = fields.Many2one(
        'stock.warehouse', 'Destination Warehouse', ondelete='cascade',
        check_company=True, states={'draft': [('readonly', False)]})
    date = fields.Datetime(
        'Date',
        default=fields.Datetime.now, index=True, tracking=True,
        states={'draft': [('readonly', False)]},
        help="Creation Date, usually the time of the order")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('transfer', 'Transfer'),
        ('validate', 'Validated'),
    ], string='Status',
        copy=False, index=True, readonly=True, store=True, tracking=True, 
       )
    transfer_line_ids = fields.One2many('stock.transit.transfer.line', 'transfer_id' ,string='Transfer Line',  states={'draft': [('readonly', False)]},)
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.advance.salary') or _('New')
        res = super(EmployeeAdvanceSalary,self).create(vals)
        return res
    

class StockwarehouseTransferLine(models.Model):
    _name = 'stock.transit.transfer.line'
    _description = 'This model is use in Stock Tansfer Line'
    
    
    product_id = fields.Many2one('product.product', 'Product', store=True)
    inventory_quantity = fields.Float(string="QOH", store=True)
    tranfer_quantity = fields.Float(string="Transfer QTY", store=True)
    received_quantity = fields.Float(string="Received Qty", store=True)
    product_uom = fields.Many2one('uom.uom', 'UOM',)
    transfer_id = fields.Many2one('stock.transit.transfer', 'Internal Transfer', store=True)
