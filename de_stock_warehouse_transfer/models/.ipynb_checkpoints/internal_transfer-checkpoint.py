# -*- coding: utf-8 -*-
from datetime import date
import time
from odoo import models, fields, api, _
from odoo import exceptions 
from odoo.exceptions import UserError, ValidationError


class StockwarehouseTransfer(models.Model):
    _name = 'stock.transit.transfer'
    _description = 'This model is use in Stock Tansfer'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    
    def picking_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'name': 'Picking',
            'domain': [('origin','=', self.name)],
            'target': 'current',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
        }
    
    def action_validate(self):
            for line in self.transfer_line_ids:
                line.received_quantity = line.tranfer_quantity
            self.write({'state': 'validate'})

    
    
    
    def action_transfer(self):
                    
        picking_internal = self.env['stock.picking.type'].search([('code', '=', 'internal'),('warehouse_id','=', self.dest_warehouse_id.id)], limit=1)
        vals = {
            'location_id': self.location_id.id,
            'location_dest_id': picking_internal.default_location_dest_id.id,
            'origin': self.name,
            'picking_type_id': picking_internal.id,
            'state': 'waiting',
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.transfer_line_ids:
            lines = {
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'name': 'Internal Transfer',
                'product_uom': line.product_id.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': picking_internal.default_location_dest_id.id,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                'product_uom_qty': line.tranfer_quantity,
            }
            stock_move = self.env['stock.move'].create(lines)

            moves = {
                'move_id': stock_move.id,
                'product_id': line.product_id.id,
                # 'product_uom': line.product_id.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': picking_internal.default_location_dest_id.id,
                # 'company_id': mv.id,
                # 'date': line.date,
                # 'lot_id':line.batch_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                'product_uom_qty': line.tranfer_quantity,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                # 'quantity_done': mv.id,
            }
            stock_move_line_id = self.env['stock.move.line'].create(moves)
            
        picking_internal = self.env['stock.picking.type'].search([('code', '=', 'internal'),('warehouse_id','=', self.source_warehouse_id.id)], limit=1)
        vals = {
            'location_id': picking_internal.default_location_src_id.id,
            'location_dest_id': self.location_id.id,
            'origin': self.name,
            'picking_type_id': picking_internal.id,
            'state': 'waiting',
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.transfer_line_ids:
            lines = {
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'name': 'Internal Transfer',
                'product_uom': line.product_id.uom_id.id,
                'location_id': picking_internal.default_location_src_id.id,
                'location_dest_id': self.location_id.id,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                'product_uom_qty': line.tranfer_quantity,
            }
            stock_move = self.env['stock.move'].create(lines)

            moves = {
                'move_id': stock_move.id,
                'product_id': line.product_id.id,
                # 'product_uom': line.product_id.uom_id.id,
                'location_id': picking_internal.default_location_src_id.id,
                'location_dest_id': self.location_id.id,
                # 'company_id': mv.id,
                # 'date': line.date,
                # 'lot_id':line.batch_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                'product_uom_qty': line.tranfer_quantity,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                # 'quantity_done': mv.id,
            }
            stock_move_line_id = self.env['stock.move.line'].create(moves)    

        self.write({'state': 'transfer'})
        
        
        
        
        
    def get_document_count(self):
        count = self.env['stock.picking'].search_count([('origin','=', self.name)])
        self.document_id = count
    
    name = fields.Char(string='Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    document_id = fields.Integer(compute='get_document_count')
    source_warehouse_id = fields.Many2one(
        'stock.warehouse', 'Source Warehouse', required=True,
 ondelete='cascade',
         states={'draft': [('readonly', False)]})
    location_id = fields.Many2one(
        'stock.location', "Transit Location",
          required=True,
        states={'draft': [('readonly', False)]})

    dest_warehouse_id = fields.Many2one(
        'stock.warehouse', 'Destination Warehouse', required=True,
 ondelete='cascade',
        states={'draft': [('readonly', False)]})
    date = fields.Datetime(
        'Date',
        default=fields.Datetime.now, index=True, tracking=True,
        states={'draft': [('readonly', False)]},
        help="Creation Date, usually the time of the order")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('transfer', 'Transfer'),
        ('validate', 'Validated'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    transfer_line_ids = fields.One2many('stock.transit.transfer.line', 'transfer_id' ,string='Transfer Line',  states={'draft': [('readonly', False)]},)
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.transit.transfer') or _('New')
        res = super(StockwarehouseTransfer,self).create(vals)
        return res
    
    def unlink(self):
        for leave in self:
            if leave.state in ('transfer','validate'):
                raise UserError(_('You cannot delete an order form  which is not draft. '))
     
            return super(StockwarehouseTransfer, self).unlink()
    

class StockwarehouseTransferLine(models.Model):
    _name = 'stock.transit.transfer.line'
    _description = 'This model is use in Stock Tansfer Line'
    
    
    product_id = fields.Many2one('product.product', 'Product', store=True)
    inventory_quantity = fields.Float(related='product_id.qty_available')
    tranfer_quantity = fields.Float(string="Transfer QTY", store=True)
    received_quantity = fields.Float(string="Received Qty", store=True, )
    
#     compute='_compute_received_qty'
    product_uom = fields.Many2one('uom.uom', 'UOM',)
    transfer_id = fields.Many2one('stock.transit.transfer', 'Internal Transfer', store=True)
    
    @api.constrains('tranfer_quantity')
    def check_quantity(self):
        if self.tranfer_quantity > self.inventory_quantity:
            raise ValidationError('Transfer Quantity must be Less than or equal to QOH.')
            
            
#     @api.depends('tranfer_quantity')
#     def _compute_received_qty(self):
#         for record in self:
#             record.received_quantity = record.tranfer_quantity
        
