# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class MrpProductionExt(models.Model):
    _inherit = 'mrp.production'

    def order_properties(self):
        self.ensure_one()
        return {
            'name': 'Order Properties',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production.properties',
            'domain': [('production_id', '=', self.id)],
        }

    def _get_report_date(self):
        for rec in self:
            order_properties = self.env['mrp.production.properties'].search([('production_id', '=', rec.id)])
            print('order', order_properties)
            return order_properties

    def _get_order_properties(self):
        for po in self:
            po_ids = self.env['mrp.production.properties'].search([('production_id', '=', po.id)])
            po.order_properties_count = len(po_ids)

    order_properties_count = fields.Integer(string='Order Properties', compute='_get_order_properties')
