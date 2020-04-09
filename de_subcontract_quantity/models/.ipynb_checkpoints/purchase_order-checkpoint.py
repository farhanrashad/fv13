# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    qty_issued = fields.Float('Issued Quantity', copy=False, compute='_compute_qty_issued', compute_sudo=True, store=True, digits='Product Unit of Measure', default=0.0)
    
    #@api.depends('qty_received', 'move_ids', 'move_dest_ids')
    def _compute_qty_issued(self):
        move_lines = self.env['stock.move.line']
        delivered_qty = 0
        #.search([('is_subcontract','=',True),('ref_sale_id','=',self.order_id.sale_id.id)])
        for line in self:
            delivered_qty = 0
            move_lines = self.env['stock.move.line'].search([('move_id.is_subcontract','=',True),('ref_sale_id','=',line.order_id.sale_id.id),('product_id','=',line.product_id.id),('state','=','done')])
            for move in move_lines:
                if move.consume_line_ids:
                    for cline in move.consume_line_ids:
                        delivered_qty += move.qty_done
            line.qty_issued = delivered_qty