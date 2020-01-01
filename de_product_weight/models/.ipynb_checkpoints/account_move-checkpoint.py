# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    is_sale_weight = fields.Boolean(related='partner_id.is_sale_weight',string='Enable Weight Pricing',readonly=True)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight Unit',readonly=True, store=True,default=1.0)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line",default=1.0)
    price_weight = fields.Float('Weight Price', required=True, digits=dp.get_precision('Weight Price'), default=1.0, domain="[('parent.is_sale_weight', '=', True)")
    
    @api.onchange('product_id','quantity')
    def _onchange_quantity(self):
        tw = 0
        for rec in self:
            if rec.sale_line_ids:
                for sale in rec.sale_line_ids:
                    tw += rec.weight * (sale.total_weight/sale.product_uom_qty)
            elif rec.purchase_line_id:
                rec.total_weight = rec.weight * (rec.purchase_line.id.total_weight/rec.purchase_line_id.product_uom_qty)
            else:
                rec.total_weight = rec.weight * rec.quantity
