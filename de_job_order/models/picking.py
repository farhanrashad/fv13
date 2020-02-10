# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp
class Picking(models.Model):
    _inherit = 'stock.picking'
    
    #job_order_id = fields.Many2one('job.order', related='purchase_id.job_order_id', string='Job Order', readonly=True, store=True)
    job_order_id = fields.Many2one("job.order", compute="_assign_sale_order", store=True, string="Job Order", readonly=True, required=False)
    ref_sale_id = fields.Many2one("sale.order",compute="_assign_sale_order", store=True, readonly=True,)
    
    def _assign_sale_order(self):
        #picking_id = self.id
        for line in self:
            query = """
        
        select p.job_order_id,j.sale_id from purchase_order p
left join job_order j on j.id = p.job_order_id
where p.id = %(purchase_id)s
union all
select j.id as job_order_id, s.id as sale_id from sale_order s
left join job_order j on j.sale_id = s.id
where s.id = %(sale_id)s
            """
            params = {
                'purchase_id': line.purchase_id.id or 0,
                'sale_id': line.sale_id.id or 0,
            }
            self.env.cr.execute(query, params=params)
            #cr = self._cr
            for order in self._cr.dictfetchall():
                line.update ({
                    'job_order_id': order['job_order_id'],
                    'ref_sale_id': order['sale_id'],
                })
        
    def _assign_sale_order1(self):
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