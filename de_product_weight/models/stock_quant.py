# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    product_weight = fields.Float('Total Weight')    
    po_uom_stk = fields.Float(string='PO UOM Stock', readonly=False, compute='_calculate_po_uom_stock', default=0.0)
    uom_po_id = fields.Many2one('uom.uom', 'PUOM',related='product_id.product_tmpl_id.uom_po_id', readonly=True)
    
    def _calculate_po_uom_stock(self):
        for rs in self:
            if rs.product_id.product_tmpl_id.uom_po_id.uom_type == 'bigger':
                rs.po_uom_stk = rs.inventory_quantity / rs.product_id.product_tmpl_id.uom_po_id.factor_inv
            elif rs.product_id.product_tmpl_id.uom_po_id.uom_type == 'smaller':
                rs.po_uom_stk = rs.inventory_quantity * rs.product_id.product_tmpl_id.uom_po_id.factor_inv
            else:
                rs.po_uom_stk = rs.inventory_quantity
                #rs.po_uom_stk = 2