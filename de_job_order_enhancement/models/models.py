# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp



class JobOrder(models.Model):
    _inherit = 'job.order'
    
    
    job_order_material_ids = fields.One2many('job.order.bom.component', 'job_order_id', string='Job Order MRP Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    
    
    def action_process(self):
        res = super(JobOrder, self).action_process()
        bom_ids = []
        all_boms = []
        for job in self:
            for sale in job.job_order_sale_lines:
                if not (sale.bom_id in bom_ids):
                    bom_ids.append(sale.bom_id)
        for boms in bom_ids:
            all_boms += boms._recursive_boms()
        
        bom_line = self.env['job.order.bom.component']
        #bom_line = self.env['job.order.mrp'].search([('bom_id', 'not in', [bom_ids])])
        for bom in all_boms:
            val = {
                'job_order_id':self.id,
                'bom_id':bom,
            }
            bom_line.create(val)
         
        for b in bom_ids:
            bom_line.search([('bom_id', '=', b.id)]).unlink()
        
        return res
      
    
    
    
    
class JobOrderBOMCompoent(models.Model):
    _name = 'job.order.bom.component'
    _description = 'Jor Order Production'
    
    #job_order_id = fields.Many2one('Job.order', string='Job Order Reference', required=True, ondelete='cascade', index=True, copy=False, readonly=True)
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    bom_id = fields.Many2one('mrp.bom', string='BOM',readonly=True)
    bom_type = fields.Selection('mrp.bom', related='bom_id.type',string='Type',readonly=True, store=True)
    quantity = fields.Float(string='Quantity',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    production_quantity = fields.Float(string='Production Quantity', compute='_calcualte_production_quantity', store=False)
    
    
    def _calcualte_production_quantity(self):
        self.production_quantity = 0
    