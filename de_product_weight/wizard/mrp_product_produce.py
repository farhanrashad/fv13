# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare, float_round, float_is_zero


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"
    
    produced_weight = fields.Float('Weight Produced', digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    @api.onchange('qty_producing')
    def _compute_produced_weight(self):
        """
        Compute the weight on change in quantity
        """
        self.produced_weight = self.qty_producing * self.product_id.weight
        
    @api.onchange('finished_lot_id')
    def onchange_finished_lot(self):
        total_qty = 0
        total_weight = 0
        for line in self.raw_workorder_line_ids:
            if line.lot_id.name == self.finished_lot_id.name:
                total_qty += line.qty_done
                total_weight += line.produced_weight
                    
                    
    def _set_quantity_done(self, qty, weight):
        """
        Set the given quantity as quantity done on the move through the move lines. The method is
        able to handle move lines with a different UoM than the move (but honestly, this would be
        looking for trouble...).
        @param qty: quantity in the UoM of move.product_uom
        """
        ml_weight = 0
        for ml in self.move_line_ids:
            ml_weight = ml.total_weight + weight
            ml_qty = ml.product_uom_qty - ml.qty_done
            if float_compare(ml_qty, 0, precision_rounding=ml.product_uom_id.rounding) <= 0:
                continue
            # Convert move line qty into move uom
            if ml.product_uom_id != self.product_uom:
                ml_qty = ml.product_uom_id._compute_quantity(ml_qty, self.product_uom, round=False)

            taken_qty = min(qty, ml_qty)
            # Convert taken qty into move line uom
            if ml.product_uom_id != self.product_uom:
                taken_qty = self.product_uom._compute_quantity(ml_qty, ml.product_uom_id, round=False)

            # Assign qty_done and explicitly round to make sure there is no inconsistency between
            # ml.qty_done and qty.
            taken_qty = float_round(taken_qty, precision_rounding=ml.product_uom_id.rounding)
            ml.qty_done += taken_qty
            if ml.product_uom_id != self.product_uom:
                taken_qty = ml.product_uom_id._compute_quantity(ml_qty, self.product_uom, round=False)
            qty -= taken_qty

            if float_compare(qty, 0.0, precision_rounding=self.product_uom.rounding) <= 0:
                break
        if float_compare(qty, 0.0, precision_rounding=self.product_uom.rounding) > 0:
            vals = self._prepare_move_line_vals(quantity=0)
            vals['qty_done'] = qty
            vals['total_weight'] = ml_weight
            ml = self.env['stock.move.line'].create(vals)
    
    def _update_finished_move(self):
        """ Update the finished move & move lines in order to set the finished
        product lot on it as well as the produced quantity. This method get the
        information either from the last workorder or from the Produce wizard."""
        production_move = self.production_id.move_finished_ids.filtered(
            lambda move: move.product_id == self.product_id and
            move.state not in ('done', 'cancel')
        )
        if production_move and production_move.product_id.tracking != 'none':
            if not self.finished_lot_id:
                raise UserError(_('You need to provide a lot for the finished product.'))
            move_line = production_move.move_line_ids.filtered(
                lambda line: line.lot_id.id == self.finished_lot_id.id
            )
            if move_line:
                if self.product_id.tracking == 'serial':
                    raise UserError(_('You cannot produce the same serial number twice.'))
                move_line.product_uom_qty += self.qty_producing
                move_line.qty_done += self.qty_producing
                move_line.total_weight += self.produced_weight
            else:
                location_dest_id = production_move.location_dest_id._get_putaway_strategy(self.product_id).id or production_move.location_dest_id.id
                move_line.create({
                    'move_id': production_move.id,
                    'product_id': production_move.product_id.id,
                    'lot_id': self.finished_lot_id.id,
                    'product_uom_qty': self.qty_producing,
                    'product_uom_id': self.product_uom_id.id,
                    'qty_done': self.qty_producing,
                    'total_weight': self.produced_weight,
                    'location_id': production_move.location_id.id,
                    'location_dest_id': location_dest_id,
                })
        else:
            rounding = production_move.product_uom.rounding
            production_move._set_quantity_done(
                float_round(self.qty_producing, precision_rounding=rounding),self.produced_weight or 0.0
            )
            
    
                
            
                        
class MRPProductProduceLine(models.TransientModel):
    _inherit = 'mrp.product.produce.line'
    
    produced_weight = fields.Float('Weight Consumed', store=True, digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    
    #api.depends('raw_product_produce_id.produced_weight','product_id','lot_id','qty_done')
    api.onchange('raw_product_produce_id.produced_weight','product_id','lot_id','qty_done')
    def _calculate_produced_weight(self):
        tw = 0
        for rs in self:
            tw = 0
            tq = 0
            if rs.product_id.product_tmpl_id.is_weight_uom:
                #if self.finished_product_produce_id.subcontract_move_id:
                if rs.move_id.bom_line_id.bom_id.type == 'normal':
                    rs.produced_weight = rs.raw_product_produce_id.produced_weight * (rs.move_id.bom_line_id.product_qty/rs.move_id.bom_line_id.bom_id.product_qty)
                else:
                    move_lines = self.env['stock.move.line'].search([('product_id', '=', rs.product_id.id),('lot_id', '=', rs.lot_id.id),('state', '=', 'done')])
                    for line in move_lines:
                        if line.location_id.usage == 'internal':
                            tw -= line.total_weight
                            tq -= line.qty_done
                        elif line.location_dest_id.usage == 'internal':
                            tw += line.total_weight
                            tq += line.qty_done
                            
                    rs.produced_weight = rs.qty_done * (tw/tq)
            else:
                rs.produced_weight = 0
            
    @api.onchange('raw_product_produce_id.produced_weight')
    def _change_produced_qty(self):
        """
        Compute the weight on change in quantity
        """
        for rs in self:
            if not(rs.product_id.product_tmpl_id.is_weight_uom):
                rs.qty_done = rs.raw_product_produce_id.produced_weight * (rs.move_id.bom_line_id.product_qty/rs.move_id.bom_line_id.bom_id.product_qty)
    
    def _update_move_lines(self):
        """ update a move line to save the workorder line data"""
        self.ensure_one()
        if self.lot_id:
            move_lines = self.move_id.move_line_ids.filtered(lambda ml: ml.lot_id == self.lot_id and not ml.lot_produced_ids)
        else:
            move_lines = self.move_id.move_line_ids.filtered(lambda ml: not ml.lot_id and not ml.lot_produced_ids)

        # Sanity check: if the product is a serial number and `lot` is already present in the other
        # consumed move lines, raise.
        if self.product_id.tracking != 'none' and not self.lot_id:
            raise UserError(_('Please enter a lot or serial number for %s !' % self.product_id.display_name))

        if self.lot_id and self.product_id.tracking == 'serial' and self.lot_id in self.move_id.move_line_ids.filtered(lambda ml: ml.qty_done).mapped('lot_id'):
            raise UserError(_('You cannot consume the same serial number twice. Please correct the serial numbers encoded.'))

        # Update reservation and quantity done
        for ml in move_lines:
            rounding = ml.product_uom_id.rounding
            if float_compare(self.qty_done, 0, precision_rounding=rounding) <= 0:
                break
            quantity_to_process = min(self.qty_done, ml.product_uom_qty - ml.qty_done)
            self.qty_done -= quantity_to_process

            new_quantity_done = (ml.qty_done + quantity_to_process)
            # if we produce less than the reserved quantity to produce the finished products
            # in different lots,
            # we create different component_move_lines to record which one was used
            # on which lot of finished product
            if float_compare(new_quantity_done, ml.product_uom_qty, precision_rounding=rounding) >= 0:
                ml.write({
                    'qty_done': new_quantity_done,
                    'lot_produced_ids': self._get_produced_lots(),
                })
            else:
                new_qty_reserved = ml.product_uom_qty - new_quantity_done
                default = {
                    'product_uom_qty': new_quantity_done,
                    'qty_done': new_quantity_done,
                    'lot_produced_ids': self._get_produced_lots(),
                }
                ml.copy(default=default)
                ml.with_context(bypass_reservation_update=True).write({
                    'product_uom_qty': new_qty_reserved,
                    'qty_done': 0
                })
            ml.write({
                'total_weight': self.produced_weight,
            })
            
    def _create_extra_move_lines(self):
        """Create new sml if quantity produced is bigger than the reserved one"""
        vals_list = []
        quants = self.env['stock.quant']._gather(self.product_id, self.move_id.location_id, lot_id=self.lot_id, strict=False)
        # Search for a sub-locations where the product is available.
        # Loop on the quants to get the locations. If there is not enough
        # quantity into stock, we take the move location. Anyway, no
        # reservation is made, so it is still possible to change it afterwards.
        for quant in quants:
            quantity = quant.quantity - quant.reserved_quantity
            quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom_id, rounding_method='HALF-UP')
            rounding = quant.product_uom_id.rounding
            if (float_compare(quant.quantity, 0, precision_rounding=rounding) <= 0 or
                    float_compare(quantity, 0, precision_rounding=self.product_uom_id.rounding) <= 0):
                continue
            vals = {
                'move_id': self.move_id.id,
                'product_id': self.product_id.id,
                'location_id': quant.location_id.id,
                'location_dest_id': self.move_id.location_dest_id.id,
                'product_uom_qty': 0,
                'product_uom_id': self.product_uom_id.id,
                'qty_done': min(quantity, self.qty_done),
                'total_weight': self.produced_weight,
                'lot_produced_ids': self._get_produced_lots(),
            }
            if self.lot_id:
                vals.update({'lot_id': self.lot_id.id})

            vals_list.append(vals)
            self.qty_done -= vals['qty_done']
            # If all the qty_done is distributed, we can close the loop
            if float_compare(self.qty_done, 0, precision_rounding=self.product_id.uom_id.rounding) <= 0:
                break

        if float_compare(self.qty_done, 0, precision_rounding=self.product_id.uom_id.rounding) > 0:
            vals = {
                'move_id': self.move_id.id,
                'product_id': self.product_id.id,
                'location_id': self.move_id.location_id.id,
                'location_dest_id': self.move_id.location_dest_id.id,
                'product_uom_qty': 0,
                'product_uom_id': self.product_uom_id.id,
                'qty_done': self.qty_done,
                'total_weight': self.produced_weight,
                'lot_produced_ids': self._get_produced_lots(),
            }
            if self.lot_id:
                vals.update({'lot_id': self.lot_id.id})

            vals_list.append(vals)

        return vals_list