# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    subcontract_move_ids = fields.One2many('stock.move', 'subcontract_order_line_id', string='Subcontract Moves', ondelete='set null', copy=False)
    
    qty_issued100 = fields.Float('Issued Quantity', copy=False, compute='_compute_qty_issued', compute_sudo=True, store=False, digits='Product Unit of Measure', default=0.0)
    weight_issued100 = fields.Float('Issued Weight', copy=False, compute='_compute_qty_issued', compute_sudo=True, store=False, digits='Product Unit of Measure', default=0.0)
    qty_issued = fields.Float(related='qty_issued100', string='Issued Qty', store=True)
    weight_issued = fields.Float(related='weight_issued100', string='Issued Weight', store=True)
    
    qty_consume100 = fields.Float('Consumed Qty', copy=False, compute='_compute_qty_consume', compute_sudo=True, store=False, digits='Product Unit of Measure', default=0.0)
    weight_consume100 = fields.Float('Consumed(Kg)', copy=False, compute='_compute_qty_consume', compute_sudo=True, store=True, digits='Product Unit of Measure', default=0.0)
    qty_consume = fields.Float(related='qty_consume100', string='Cons.Qty', store=True)
    weight_consume = fields.Float(related='weight_consume100', string='Cons.Wght', store=True)

    
    
    @api.depends('move_ids.move_orig_ids.production_id.move_raw_ids.state', 'move_ids.move_orig_ids.production_id.move_raw_ids.product_uom_qty', 'move_ids.move_orig_ids.production_id.move_raw_ids.product_uom')
    def _compute_qty_consume(self):
        #super(PurchaseOrderLine, self)._compute_qty_consume()
        for line in self:
            total = 0.0
            total_weight = 0.0
            for move in line.move_ids.move_orig_ids.production_id.move_raw_ids:
                if move.state == 'done':
                    total += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                    total_weight = move.total_weight
            line.qty_consume100 = total
            line.weight_consume100 = total_weight
         
    @api.depends('subcontract_move_ids')
    def _compute_qty_issued(self):
        #self.ensure_one()
        #move_references = self.move_ids.mapped('reference')
        for line in self:
            sum_qty = 0
            sum_weight = 0
            for move in line.subcontract_move_ids:
                sum_qty += move.quantity_done
                sum_weight += move.total_weight
            line.qty_issued100 = sum_qty
            line.weight_issued100 = sum_weight
