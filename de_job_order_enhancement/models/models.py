# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp
import threading


class JobOrder(models.Model):
    _inherit = 'job.order'
    
    
#     def campaign_thread(self, from_date=None, to_date=None):
#         try:
#             is_active = False
#             threads = threading.enumerate()
#             for thread in threads:
#                 if thread.name == 'import_campaign':
#                     is_active = True
#             if not is_active:
#                 self.campaign_manual = True
#                 self.env.cr.commit()
#                 thread = threading.Thread(name='import_campaign', target=self.action_process)                
#                 thread.start()
#         except Exception as e:
#             raise ValidationError(str(e))
    
    
    job_order_material_ids = fields.One2many('job.order.bom.component', 'job_order_id', string='Job Order MRP Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)

    
    
    def action_process(self):
        res = super(JobOrder, self).action_process()
        product_list = []
        bom_product = []
        all_boms = []
        for sale in self.job_order_sale_lines:
            product_bom = self.env['mrp.bom'].search([('product_id','=',sale.product_id.id)])
            bom_vals =   {
                     'job_order_id':  self.name,
                     'product_id': product_bom.product_id.id,
                     'type': product_bom.type,
                       }  
            bom_product.append(bom_vals)
            for component_level1 in product_bom.bom_line_ids:
#                 product_bom_vals =   {
#                      'job_order_id':  self.name,
#                      'product_id': component_level1.product_id.name,
#                      'type': product_bom.type,
#                        }                 
                product_list.append(component_level1.product_id.name)
#                 for product in product_list:
                component_bom_level2 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level1.product_id.name)])
                if component_bom_level2:
                    for component_level2 in component_bom_level2.bom_line_ids:
                        product_list.append(component_level2.product_id.name)
                        component_bom_level3 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level2.product_id.name)])
                        if component_bom_level3:
                            for component_level3 in component_bom_level3.bom_line_ids:
                                product_list.append(component_level3.product_id.name)
                                component_bom_level4 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level3.product_id.name)])
                                if component_bom_level4:
                                    for component_level4 in component_bom_level4.bom_line_ids:
                                        product_list.append(component_level4.product_id.name)
                                        component_bom_level5 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level4.product_id.name)])
                                        if component_bom_level5:
                                            for component_level5 in component_bom_level5.bom_line_ids:
                                                product_list.append(component_level5.product_id.name)
                                                component_bom_level6 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level5.product_id.name)])
                                                if component_bom_level6:
                                                    for component_level6 in component_bom_level6.bom_line_ids:
                                                        product_list.append(component_level6.product_id.name)
                                                        component_bom_level7 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level6.product_id.name)])
                                                        if component_bom_level7:
                                                            for component_level7 in component_bom_level7.bom_line_ids:
                                                                product_list.append(component_level7.product_id.name)

        bom_products = set(product_list)
        for product in bom_products:
#             component_boms = self.env['mrp.bom'].search([('product_tmpl_id.name','=',product)])

            component_boms = self.env['product.product'].search([('name','=',product)])
            for component in component_boms:
                bom_vals =   {
                                 'job_order_id':  self.name,
                                 'product_id': component.id,
#                                  'type': component.bom_id.type,
                                   }  
                bom_product.append(bom_vals)
            
        for product in bom_product:
            all_boms.append((0,0,{
                            'job_order_id':  product['job_order_id'],
                            'product_id': product['product_id'],
#                             'type': product['type'],
                            })) 
#             bom_product.append(bom_vals)
            
        self.job_order_material_ids = all_boms             
           
        return res

    
#     def action_process(self):
#         res = super(JobOrder, self).action_process()
#         bom_ids = []
#         all_boms = []
#         for job in self:
#             for sale in job.job_order_sale_lines:
#                 if not (sale.bom_id in bom_ids):
#                     bom_ids.append(sale.bom_id)
#         for boms in bom_ids:
#             all_boms += boms._recursive_boms()
        
#         bom_line = self.env['job.order.bom.component']
#         #bom_line = self.env['job.order.mrp'].search([('bom_id', 'not in', [bom_ids])])
#         for bom_prod in bom_ids:
#             product_bom = self.env['product.product'].search([('id','=',bom_prod.id)])
        
        
#             for bom in product_bom:
#                 val = {
#                     'job_order_id':self.id,
#                     'name':bom.name,
# #                     'type': bom.type,
#                 }
#                 bom_line.create(val)
   
        
#         return res
      
    
    
    
    
class JobOrderBOMCompoent(models.Model):
    _name = 'job.order.bom.component'
    _description = 'Jor Order Production'
    
    #job_order_id = fields.Many2one('Job.order', string='Job Order Reference', required=True, ondelete='cascade', index=True, copy=False, readonly=True)
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
#     name = fields.Char(string="Name")
    product_id = fields.Many2one('product.product', string='Produt',readonly=True)
#     product_tmpl_id = fields.Many2one('product.template', string='Product')
    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit'),
        ('subcontract', 'Subcontracting')
          ], 'BoM Type',
        default='normal')
    quantity = fields.Float(string='Quantity',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    production_quantity = fields.Float(string='Production Quantity', compute='_calcualte_production_quantity', store=False)
    
    
    def _calcualte_production_quantity(self):
        self.production_quantity = 0
    