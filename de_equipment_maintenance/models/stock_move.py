# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    reserved_availability = fields.Float(
        'Reserved', compute='_compute_reserved_availability',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Quantity that has already been reserved for this move')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    emm_order_id = fields.Many2one('maintenance.order', 'Maintenance Order', index=True)
    show_operations = fields.Boolean(compute='_compute_show_operations')
    show_details_visible = fields.Boolean('Details Visible', compute='_compute_show_details_visible')
    has_tracking = fields.Selection(related='product_id.tracking', string='Product with Tracking', readonly=True)
    picking_id = fields.Many2one('stock.picking', 'Transfer Reference', index=True)
    origin_returned_move_id = fields.Many2one(
        'stock.move', 'Origin return move',
    )
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
    )
    product_uom_category_id = fields.Many2one(comodel_name='uom.category', related='product_id.uom_id.category_id')

    product_qty = fields.Float(
        'Quantity', compute='_compute_product_qty')

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_product_qty(self):
        self.ensure_one()
        rounding_method = self._context.get('rounding_method', 'UP')
        self.product_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.product_id.uom_id,
                                                              rounding_method=rounding_method)

    @api.depends('move_line_ids.product_qty')
    def _compute_reserved_availability(self):
        """ Fill the `availability` field on a stock move, which is the actual reserved quantity
        and is represented by the aggregated `product_qty` on the linked move lines. If the move
        is force assigned, the value will be 0.
        """
        result = {data['move_id'][0]: data['product_qty'] for data in
                  self.env['stock.move.line'].read_group([('move_id', 'in', self.ids)], ['move_id', 'product_qty'],
                                                         ['move_id'])}
        for rec in self:
            rec.reserved_availability = rec.product_id.uom_id._compute_quantity(result.get(rec.id, 0.0),
                                                                                rec.product_uom,
                                                                                rounding_method='HALF-UP')

    @api.depends('picking_type_id.show_operations')
    def _compute_show_operations(self):
        for picking in self:
            if self.env.context.get('force_detailed_view'):
                picking.show_operations = True
                continue
            if picking.picking_type_id.show_operations:
                if (picking.state == 'draft' and picking.immediate_transfer) or picking.state != 'draft':
                    picking.show_operations = True
                else:
                    picking.show_operations = False
            else:
                picking.show_operations = False

    def action_show_details(self):
        """ Returns an action that will open a form view (in a popup) allowing to work on all the
        move lines of a particular move. This form view is used when "show operations" is not
        checked on the picking type.
        """
        self.ensure_one()

        # If "show suggestions" is not checked on the picking type, we have to filter out the
        # reserved move lines. We do this by displaying `move_line_nosuggest_ids`. We use
        # different views to display one field or another so that the webclient doesn't have to
        # fetch both.
        if self.picking_id.picking_type_id.show_reserved:
            view = self.env.ref('stock.view_stock_move_operations')
        else:
            view = self.env.ref('stock.view_stock_move_nosuggest_operations')

        picking_type_id = self.picking_type_id or self.picking_id.picking_type_id
        return {
            'name': _('Detailed Operations'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.move',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'context': dict(
                self.env.context,
                show_lots_m2o=self.has_tracking != 'none' and (
                        picking_type_id.use_existing_lots or self.origin_returned_move_id.id),
                # able to create lots, whatever the value of ` use_create_lots`.
                show_lots_text=self.has_tracking != 'none' and picking_type_id.use_create_lots and not picking_type_id.use_existing_lots and self.state != 'done' and not self.origin_returned_move_id.id,
                show_source_location=self.location_id.child_ids and self.picking_type_id.code != 'incoming',
                show_destination_location=self.location_dest_id.child_ids and self.picking_type_id.code != 'outgoing',
                show_package=not self.location_id.usage == 'supplier',
                show_reserved_quantity=self.state != 'done'
            ),
        }

    @api.depends('product_id', 'has_tracking')
    def _compute_show_details_visible(self):
        """ According to this field, the button that calls `action_show_details` will be displayed
        to work on a move from its picking form view, or not.
        """
        has_package = self.user_has_groups('stock.group_tracking_lot')
        multi_locations_enabled = self.user_has_groups('stock.group_stock_multi_locations')
        consignment_enabled = self.user_has_groups('stock.group_tracking_owner')

        show_details_visible = multi_locations_enabled or consignment_enabled or has_package

        for move in self:
            if not move.product_id:
                move.show_details_visible = False
            else:
                move.show_details_visible = ((show_details_visible or move.has_tracking != 'none') and
                                             move.picking_id.picking_type_id.show_operations is False)

