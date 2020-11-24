# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.addons import decimal_precision as dp
import threading


class JobOrder(models.Model):
    _inherit = 'job.order'
    
    def action_material_planning(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
#             'multi': False,
            'name': 'Material Planning',
            'domain': [('job_order_id','=', self.id)],
            'target': 'current',
            'res_model': 'job.order.bom.component',
            'view_mode': 'tree,form',
        }
    
    
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
       # SO  product bom     
            bom_vals =   {
                     'job_order_id':  self.name,
                     'product_id': product_bom.product_id.id,
                     'type': product_bom.type,
                     'quantity':  product_bom.product_qty,
#                      'vendor_id': for vendor in component_bom_level1_type.subcontractor_ids.id: return vendor 
                       }  
            bom_product.append(bom_vals)
            for component_level1 in product_bom.bom_line_ids:   
        # Level 1         
                product_list.append(component_level1.product_id.name)
                component_bom_level1_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level1.product_id.name)])
                bom_vals =   {
                     'job_order_id':  self.name,
                     'product_id': component_level1.product_id.id,
                     'type': component_bom_level1_type.type,
                     'quantity':  component_level1.product_qty,
                     'vendor_id': [vendor for vendor in component_bom_level1_type.subcontractor_ids] 
                           }  
                bom_product.append(bom_vals) 
                component_bom_level2 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level1.product_id.name)])
         # Level 2       
                if component_bom_level2:
                    for component_level2 in component_bom_level2.bom_line_ids:
                        product_list.append(component_level2.product_id.name)
                        component_bom_level2_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level2.product_id.name)])
                        bom_vals =   {
                         'job_order_id':  self.name,
                         'product_id': component_level2.product_id.id,
                         'type': component_bom_level2_type.type,
                         'quantity':  component_level2.product_qty,
                         'vendor_id': [vendor for vendor in  component_bom_level2_type.subcontractor_ids] 
                           }  
                        bom_product.append(bom_vals) 
                        component_bom_level3 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level2.product_id.name)])
         # Level 3       
                        if component_bom_level3:
                            for component_level3 in component_bom_level3.bom_line_ids:
                                product_list.append(component_level3.product_id.name)
                                component_bom_level3_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level3.product_id.name)])
                                bom_vals =   {
                                 'job_order_id':  self.name,
                                 'product_id': component_level3.product_id.id,
                                 'type': component_bom_level3_type.type,
                                 'quantity':  component_level3.product_qty,
                                 'vendor_id': [vendor for vendor in  component_bom_level3_type.subcontractor_ids] 
                                   }  
                                bom_product.append(bom_vals) 
                                
                                component_bom_level4 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level3.product_id.name)])
                         # Level 4       
                                
                                if component_bom_level4:
                                    for component_level4 in component_bom_level4.bom_line_ids:
                                        product_list.append(component_level4.product_id.name)
                                        
                                        component_bom_level4_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level4.product_id.name)])
                                        bom_vals =   {
                                         'job_order_id':  self.name,
                                         'product_id': component_level4.product_id.id,
                                         'type': component_bom_level4_type.type,
                                         'quantity':  component_level4.product_qty,
                                         'vendor_id': [vendor for vendor in  component_bom_level4_type.subcontractor_ids] 
                                           }  
                                        bom_product.append(bom_vals) 
                         # Level 5       
                                        component_bom_level5 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level4.product_id.name)])
                                        if component_bom_level5:
                                            for component_level5 in component_bom_level5.bom_line_ids:
                                                product_list.append(component_level5.product_id.name)
                                                component_bom_level5_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level5.product_id.name)])
                                                bom_vals =   {
                                                 'job_order_id':  self.name,
                                                 'product_id': component_level5.product_id.id,
                                                 'type': component_bom_level5_type.type,
                                                 'quantity':  component_level5.product_qty,
                                                 'vendor_id': [vendor for vendor in  component_bom_level5_type.subcontractor_ids] 
                                                   }  
                                                bom_product.append(bom_vals) 
                                                
                           # Level 6       
                                                component_bom_level6 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level5.product_id.name)])
                                                if component_bom_level6:
                                                    for component_level6 in component_bom_level6.bom_line_ids:
                                                        product_list.append(component_level6.product_id.name)
                                                        component_bom_level6_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level6.product_id.name)])
                                                        bom_vals =   {
                                                         'job_order_id':  self.name,
                                                         'product_id': component_level6.product_id.id,
                                                         'type': component_bom_level6_type.type,
                                                         'quantity':  component_level6.product_qty,
                                                         'vendor_id': [vendor for vendor in  component_bom_level6_type.subcontractor_ids] 
                                                         }  
                                                        bom_product.append(bom_vals)
                                                
                                # Level 7       
                                                        component_bom_level7 = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level6.product_id.name)])
                                                        if component_bom_level7:
                                                            for component_level7 in component_bom_level7.bom_line_ids:
                                                                product_list.append(component_level7.product_id.name)
                                                                component_bom_level7_type = self.env['mrp.bom'].search([('product_tmpl_id.name','=',component_level7.product_id.name)])
                                                                bom_vals =   {
                                                                'job_order_id':  self.name,
                                                                'product_id': component_level7.product_id.id,
                                                                'type': component_bom_level7_type.type,
                                                               'quantity':  component_level7.product_qty,
                                                               'vendor_id': [vendor for vendor in   component_bom_level7_type.subcontractor_ids] 
                                                                   }  
                                                                bom_product.append(bom_vals)
                                                                

#         bom_products = set(product_list)
#         for product in product_list:
# #             component_boms = self.env['mrp.bom'].search([('product_tmpl_id.name','=',product)])

#             component_boms = self.env['product.product'].search([('name','=',product)])
#             for component in component_boms:
#                 bom_vals =   {
#                                  'job_order_id':  self.name,
#                                  'product_id': component.id,
# #                                  'type': component.bom_id.type,
#                                    }  
#                 bom_product.append(bom_vals)
            
        for product in bom_product:
            all_boms.append((0,0,{
                            'job_order_id':  product['job_order_id'],
                            'product_id': product['product_id'],
                            'type': product['type'],
                            'quantity': product['quantity'], 
#                             'vendor_id': product['vendor_id'],    
                            })) 
            
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
    
    def unlink(self):
        for leave in self:
            if leave.po_created == True   or leave.po_created == False:
                raise UserError(_('You cannot delete an order'))
     
            return super(JobOrderBOMCompoent, self).unlink()
    
    
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    po_created = fields.Boolean(string="PO Created")
    product_id = fields.Many2one('product.product', string='Produt',readonly=True)
    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit'),
        ('subcontract', 'Subcontracting')
          ], 'BoM Type',
        default='normal')
    quantity = fields.Float(string='Quantity',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    production_quantity = fields.Float(string='Production Quantity', store=False)
    
    
#      compute='_calcualte_production_quantity',
    
    def _calcualte_production_quantity(self):
        self.production_quantity = 0    
    
    
    def action_generate_po(self):
#         for line in self:
#             if line.partner_id:
#                 pass
#             else:
#                 raise UserError(_('Please Select Vendor for all selected lines.'))
        vendor_list = []
        for line in self:
            if line.partner_id and line.po_created == False:
                vendor_list.append(line.partner_id)
            else:
                pass
        list = set(vendor_list)
        for te in list:
            product = []
            for re in self:
                if te == re.partner_id:
                    if re.po_created == False:
                        valss = {
                            'product_id': re.product_id.id,
                            'name': re.product_id.name,
                            'product_uom_qty': re.product_uom_qty_order,
                            'price_unit': re.product_id.standard_price,
                            'date_planned': fields.Date.today(),
                            'product_uom': re.product_id.uom_po_id.id,
                        }
                        product.append(valss)
            vals = {
                  'partner_id': te.id,
                  'date_order': fields.Date.today(),
                  'sale_ref_id': self.mo_id.sale_id.name,
                  'origin': self.mo_id.name,
                    }
            order = self.env['purchase.order'].create(vals)
            for test in product:
                order_line = {
                       'order_id': order.id,
                       'product_id': test['product_id'],
                       'name': test['name'],
                       'product_qty': test['product_uom_qty'],
                       'price_unit': test['price_unit'],
                       'date_planned': fields.Date.today(),
                       'product_uom': test['product_uom'],
                        }
                orders_lines = self.env['purchase.order.line'].create(order_line)
        for line in self:
            if line.po_process == True and not line.partner_id==' ':
                line.update ({
                   'po_process': False,
                    'po_created': True,
                  	})
                
                
    