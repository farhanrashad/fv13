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
    
    def action_confirm(self):
        res = super(JobOrder, self).action_confirm()
        for line in self.sale_id.order_line:
            for order_line in self.job_order_sale_lines:
                if order_line.product_id.id == line.product_id.id:
                    order_line.update({
                        'unit_weight': line.weight
                    })
        return res
    
    
    
    
    
    
    
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
            sale_product = sale.product_id.id
            order_qty = sale.product_uom_qty
            unit_weight = sale.unit_weight
            yarn_qty = 0.0
                
            for rule in self.struct_id.rule_ids:
                if rule.code=='HWP':
                    yarn_qty = 1 + (rule.quantity_percentage/100)
                
            greige_qty = 0.0
                
            for rule in self.struct_id.rule_ids:
                if rule.code=='DWP':
                    greige_qty = 1 + (rule.quantity_percentage/100)
            product_bom = self.env['mrp.bom'].search([('product_id','=',sale.product_id.id)])
       # SO  product bom
            variant_qty = 0.0
                
            for rule in self.struct_id.rule_ids:
                if rule.code=='BGP':
                    variant_qty = 1 + (rule.quantity_percentage/100)
                
            bom_vals =   {
                     'job_order_id':  self.name,
                     'product_id': product_bom.product_id.id,
                     'type': product_bom.type,
                     'quantity':  product_bom.product_qty,
                     'production_quantity': order_qty * variant_qty,
                     'weight':  unit_weight * order_qty * variant_qty,
                     'source_product_id': sale_product,
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
                         'production_quantity': order_qty * variant_qty,
                         'weight':  unit_weight * order_qty * variant_qty,
                         'source_product_id': sale_product,
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
                             'production_quantity': order_qty * variant_qty,
                             'weight':   unit_weight * order_qty * variant_qty * greige_qty,
                             'source_product_id': sale_product,
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
                                     'production_quantity':  component_level3.product_qty * yarn_qty * unit_weight * order_qty * greige_qty,
                                     'weight': unit_weight * order_qty * variant_qty * greige_qty,
                                     'source_product_id': sale_product,
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
                                             'production_quantity':  component_level4.product_qty * yarn_qty * unit_weight * order_qty * greige_qty,
                                            'weight': unit_weight * order_qty * variant_qty * greige_qty,
                                             'source_product_id': sale_product,
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
                                                     'production_quantity':  component_level5.product_qty * yarn_qty * unit_weight * order_qty * greige_qty,
                                                      'weight': unit_weight * order_qty * variant_qty * greige_qty,
                                                     'source_product_id': sale_product,

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
                                                              'production_quantity':  component_level6.product_qty * yarn_qty * unit_weight * order_qty * greige_qty,
                                                              'weight':  unit_weight * order_qty * greige_qty,
                                                             'source_product_id': sale_product,
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
                                                                    'source_product_id': sale_product,
                                                                       }  
                                                                bom_product.append(bom_vals)
                                                            
                                                                    
                                                                
                                                                

            
        for product in bom_product:
            all_boms.append((0,0,{
                            'job_order_id':  product['job_order_id'],
                            'product_id': product['product_id'],
                            'type': product['type'],
                            'quantity': product['quantity'],
                            'weight': product['weight'],
                            'production_quantity': product['production_quantity'],  
                            'source_product_id': product['source_product_id']
                            })) 
            
        self.job_order_material_ids = all_boms             
        for product in self.job_order_material_ids:
            line_product = []
            product_values = self.env['product.product'].search([('id','=',product.product_id.id)])
            for vendor in product_values.seller_ids:
                line_product.append(vendor.name.id)
            if product.type != 'normal':
               product.update({
                   'vendor_id': line_product[0],
#                    'source_product_id': product.product_id.id
               }) 
                
        return res

    

    
class JobOrderLine(models.Model):
    _inherit = 'job.order.sale.line'
    
    
    unit_weight = fields.Float(string='Unit Weight')
      
    
    
    
    
class JobOrderBOMCompoent(models.Model):
    _name = 'job.order.bom.component'
    _description = 'Jor Order Production'
    
    def _default_picking_type(self):
        return self.env['stock.picking.type'].search([
            ('code', '=', 'mrp_operation'),],
            limit=1).id
    
    def _default_src_location(self):
        return self.env['stock.location'].search([
            ('name', '=', 'Stock'),],
            limit=1).id
    
    def _default_dest_location(self):
        return self.env['stock.location'].search([
            ('name', '=', 'Stock'),],
            limit=1).id
    
    def _default_company(self):
        return self.env['res.company'].search([
            ('name', '=', 'Al-Ghani International'),],
            limit=1).id
    
    def unlink(self):
        for leave in self:
            if leave.po_created == True   or leave.po_created == False:
                raise UserError(_('You cannot delete an order'))
     
            return super(JobOrderBOMCompoent, self).unlink()
    
    
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', string='Vendor', index=True)
    po_created = fields.Boolean(string="PO Created")
    production_created = fields.Boolean(string="MO Created")
    product_id = fields.Many2one('product.product', string='Product',readonly=True)
    category_id = fields.Many2one(related='product_id.categ_id')
    source_product_id = fields.Many2one('product.product', string='Source Product',readonly=True)
    weight = fields.Float(string='Weight',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit'),
        ('subcontract', 'Subcontracting')
          ], 'BoM Type',
        default='normal')
    quantity = fields.Float(string='BOM Quantity',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    production_quantity = fields.Float(string='Production Quantity')
    company_id = fields.Many2one('res.company', store=True, string='Company', readonly=False, default=_default_company,)
    location_src_id = fields.Many2one('stock.location', 'From', check_company=True, default=_default_src_location,)
    location_dest_id = fields.Many2one('stock.location', 'To', check_company=True, default=_default_dest_location,)
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
         readonly=True, default=_default_picking_type,)
    


    
    
#      compute='_calcualte_production_quantity',
    
    def _calcualte_production_quantity(self):
        self.production_quantity = 0  
        
        
    def action_generate_production_order(self):
        for line in self:
            if line.production_created == False and line.type == 'normal':
                line_bom = self.env['mrp.bom'].search([('product_tmpl_id.name','=',line.product_id.name)])
                for bom in line_bom:
                    line__bom_vals = []
                    for component in bom.bom_line_ids:
                        line__bom_vals.append((0,0, {
                                'product_id': component.product_id.id,
                                'name': component.product_id.name,
                                'product_uom': component.product_id.uom_po_id.id,
                                'product_uom_qty': component.product_qty,
                                'date': fields.Date.today(),
                                'date_expected': fields.Date.today(),
                                'location_id': line.location_src_id.id,
                                'location_dest_id': line.location_dest_id.id,
                        }))
                production_vals ={
                        'product_id': line.product_id.id,
                        'product_uom_id': line.product_id.uom_id.id,
                        'product_qty': line.quantity,
                        'origin': self.job_order_id.name, 
                        'job_order_id': self.job_order_id.id, 
                        'bom_id': line_bom[0].id,
                        'date_planned_start': fields.Date.today(),
                        'picking_type_id': line.picking_type_id.id,
                        'location_src_id': line.location_src_id.id,
                        'location_dest_id': line.location_dest_id.id,
                        'move_raw_ids': line__bom_vals ,
                }
                production_order = self.env['mrp.production'].create(production_vals)
                if line.production_created == False and line.type == 'normal':
                    line.update ({
#                    'po_process': False,
                        'production_created': True,
                        })
                
          
    
    
    
    def action_generate_po(self):
        vendor_list = []
        for line in self:
            if line.vendor_id and line.po_created == False:
                vendor_list.append(line.vendor_id)
            else:
                pass
        list = set(vendor_list)
        for vendor in list:
            product = []
            for seller_line in self:
                if vendor == seller_line.vendor_id:
                    if seller_line.po_created == False:
                        line_vals = {
                            'product_id': seller_line.product_id.id,
                            'name': seller_line.product_id.name,
                            'product_uom_qty': seller_line.quantity,
                            'price_unit': seller_line.product_id.standard_price,
                            'date_planned': fields.Date.today(),
                            'product_uom': seller_line.product_id.uom_po_id.id,
                        }
                        product.append(line_vals)
            vals = {
                  'partner_id': vendor.id,
                  'date_order': fields.Date.today(),
                  'job_order_id': self.job_order_id.id,
                  'origin': self.job_order_id.name,
                    }
            order = self.env['purchase.order'].create(vals)
            for prod in product:
                order_line = {
                       'order_id': order.id,
                       'product_id': prod['product_id'],
                       'name': prod['name'],
                       'product_qty': prod['product_uom_qty'],
                       'price_unit': prod['price_unit'],
                       'date_planned': fields.Date.today(),
                       'product_uom': prod['product_uom'],
                        }
                purchase_orders_line = self.env['purchase.order.line'].create(order_line)
        for line in self:
            if line.po_created == False and line.type != 'normal' and line.vendor_id:
                line.update ({
                    'po_created': True,
                  	})
                
                
    