# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
   
    routing_f_id = fields.Many2one(
        'mrp.routing', srting='Routing', store=True)
    routing_s_id = fields.Many2one(
        'mrp.routing', string='Routing', store=True)
    routing_t_id = fields.Many2one(
        'mrp.routing', string='Routing', store=True)
    routing_fo_id = fields.Many2one(
        'mrp.routing', string='Routing', store=True)
    product_f_qty = fields.Float(string='Quantity To Produce')
    product_s_qty = fields.Float(string='Quantity To Produce')
    product_t_qty = fields.Float(string='Quantity To Produce')
    product_fo_qty = fields.Float(string='Quantity To Produce')
    
    
                
    def button_plans(self):
        """ Create work orders. And probably do stuff, like things. """
        orders_to_plan = self.filtered(lambda order: order.routing_f_id and order.state == 'confirmed')
        for order in orders_to_plan:
            order.move_raw_ids.filtered(lambda m: m.state == 'draft')._action_confirm()
            quantity = self.product_f_qty
            boms, lines = order.bom_id.explode(order.product_id, quantity, picking_type=order.bom_id.picking_type_id)
            order._generate_workorders(boms)
            order._plan_workorders()
        return True
        
    
    def _prepare_workorder_vals(self, operation, workorders, quantity):
        self.ensure_one()
        data = {
            'name': operation.name,
            'production_id': self.id,
            'workcenter_id': operation.workcenter_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'operation_id': operation.id,
            'state':'ready' or 'pending',
            'qty_producing': quantity,
            'consumption': self.bom_id.consumption,
        }
        return data
#     def action_confirm(self):
#         self._check_company()
#         for production in self:
#             if not production.move_raw_ids:
#                 raise UserError(_("Add some materials to consume before marking this MO as to do."))
#             for move_raw in production.move_raw_ids:
#                 move_raw.write({
#                     'unit_factor': move_raw.product_uom_qty / production.product_f_qty,
#                 })
#             production._generate_finished_moves()
#             production.move_raw_ids._adjust_procure_method()
#             (production.move_raw_ids | production.move_finished_ids)._action_confirm()
#         for production in self:
#             if not production.move_raw_ids:
#                 raise UserError(_("Add some materials to consume before marking this MO as to do."))
#             for move_raw in production.move_raw_ids:
#                 move_raw.write({
#                     'unit_factor': move_raw.product_uom_qty / production.product_f_qty,
#                 })
#             production._generate_finished_moves()
#             production.move_raw_ids._adjust_procure_method()
#             (production.move_raw_ids | production.move_finished_ids)._action_confirm()   
#         return True
