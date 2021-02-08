from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp
import threading


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    stock_total_weight = fields.Float(string='Material Weight') 
    total_weight = fields.Float('Total Weight', store=False, digits=dp.get_precision('Stock Weight'), compute='_calculate_total_weight', readonly=True)
            
    @api.depends('move_line_ids','move_line_nosuggest_ids','product_id')
    def _calculate_total_weight(self):
        for line in self:
            sum_weight = sum_weight1 = 0
            for move_line in line.move_line_ids:
                if not move_line.total_weight:
                    sum_weight += move_line.qty_done * move_line.weight
                else:
                    sum_weight += move_line.total_weight
            line.total_weight = line.stock_total_weight
