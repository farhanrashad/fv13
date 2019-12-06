# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    #weight_available = fields.Float(compute='_compute_total_weight', string='Weight Available', readonly=True, store=True)
    weight_available = fields.Float(string='Weight Available')
    is_weight_uom = fields.Boolean('Weight UOM',default=True)
    weight_done = fields.Float('Weight Done')
    
    @api.depends(
		'product_variant_ids',
		'product_variant_ids.stock_move_ids.product_qty',
		'product_variant_ids.stock_move_ids.state',
	)
    @api.depends_context('company_owned', 'force_company')
    def _compute_total_weight(self):
        """
        Compute the total weight of physical storeage locations
        """
		#product_ids = self.env['product.product'].search([('product_tmpl_id', '=', rs.id)])
		#move_lines = self.env['stock.move.line'].search([('product_id', '=', product_id.id)])
        total_weight = 0
        for product in self.product_variant_ids:
            for mv in product.stock_move_ids:
                total_weight += mv.total_weight
                
        self.weight_available = total_weight
		