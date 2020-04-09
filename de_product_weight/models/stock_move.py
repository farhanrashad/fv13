# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), compute='_calculate_total_weight', readonly=True)
    
    def _get_total_weight1(self):
        select = 0
        from_clause, where_clause, where_clause_params = ''
        move_line_obj = self.env['stock.move.line']
        for line in self:
            if len(line.move_line_ids):
                domain = [('product_id', '=', line.product_id.id),
                          ('state', '=', 'done'),
                          
                          ]

                where_query = move_line_obj._where_calc(domain)
                move_line_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT SUM(total_weight) from " + from_clause + " where " + where_clause

            self.env.cr.execute(select, where_clause_params)
            line.total_weight = self.env.cr.fetchone()[0] or 0.0
            
    @api.depends('move_line_ids','move_line_nosuggest_ids','product_id')
    def _calculate_total_weight(self):
        sum_weight = sum_weight1 = 0
        for line in self:
            for move_line in line.move_line_ids:
                sum_weight += move_line.qty_done * move_line.weight
            for move_line1 in line.move_line_nosuggest_ids:
                sum_weight1 += move_line1.qty_done * move_line.weight
            line.total_weight = sum_weight or sum_weight1
            
    #@api.depends('move_line_ids')
    def _get_total_weight(self):
        for mv in self:
            sum_weight = 0.0
            for line in mv.move_line_ids:
                if line.location_id.id == mv.location_id.id:
                    sum_weight += line.total_weight
            mv.update({
                'total_weight': sum_weight
            })
    
    
    #@api.depends('product_id','quantity_done')
	#def _get_total_weight(self):
		#for line in self.move_line_ids:
			#if self.product_id == line.product_id:
				#self.total_weight = line.total_weight
			
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), readonly=False, compute="_calculate_total_weight", help="Weight of the product in order line")
    
    @api.depends('product_id','lot_id','qty_done', 'weight')
    def _calculate_total_weight(self):
        for line in self:
            line.total_weight = line.qty_done * line.weight
            
    @api.onchange('product_id','lot_id')
    def onchange_product(self):
        if self.lot_id:
            self.qty_done = self.lot_id.product_qty
                
        
    def write(self, vals):
        #Raw Material Assignment
        res = super(StockMoveLine, self).write(vals)
        #self.product_id.product_tmpl_id.weight_available = self.product_id.product_tmpl_id.weight_available + self.total_weight
        for rs in self.filtered(lambda x: x.move_id.state in ('done')):
            if rs.product_id.product_tmpl_id.is_weight_uom:
                if rs.location_dest_id.usage == 'internal':
                    rs.product_id.weight_available += rs.total_weight
                    if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        rs.lot_id.product_weight += rs.total_weight
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_dest_id.id),('lot_id', '=', rs.lot_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.lot_id.product_weight
                        })
                    else:
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_dest_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.total_weight
                        }) 
                elif rs.location_id.usage == 'internal':
                    rs.product_id.weight_available -= rs.total_weight
                    if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        rs.lot_id.product_weight -= rs.total_weight
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_id.id),('lot_id', '=', rs.lot_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.lot_id.product_weight
                        })
                    else:
                        quant = self.env['stock.quant'].search([('product_id', '=', rs.product_id.id),('location_id', '=', rs.location_id.id)])
                        quant.sudo().write({
                            'product_weight':rs.total_weight
                        }) 
                    
                #if rs.location_id.usage == 'internal':
                    #rs.product_id.product_tmpl_id.weight_available = rs.total_weight
                    #if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        #rs.lot_id.product_weight -= rs.total_weight
                #elif rs.location_dest_id == 'internal':
                    #rs.product_id.product_tmpl_id.weight_available = rs.product_id.product_tmpl_id.weight_available + rs.total_weight
                    #if not (rs.product_id.product_tmpl_id.tracking) == 'none':
                        #rs.lot_id.product_weight += rs.total_weight
                    
        return res