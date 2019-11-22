# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    parent_product_tmpl_id = fields.Many2one('product.template', 'Parent Product', stored=True, required=False)
    ref_product_tmpl_id = fields.Many2one('product.template', 'Reference Product', stored=True, required=False)
    ref_product_tmpl_ids = fields.One2many('product.template', 'ref_product_tmpl_id', string='Reference Products', auto_join=True)
    
    data_maintenance_lines = fields.One2many('product.data.maintain', 'product_tmpl_id', string='Maintenance Lines',  copy=True, auto_join=True)
    
    def action_create_master_data(self):
        self.bom_ids.unlink()
        for p in self.ref_product_tmpl_ids:
            p.bom_ids.unlink()
        self.ref_product_tmpl_ids.unlink()
        for vn in self.product_variant_ids:
            parent_product_tmpl_id = self.id
            for dm in self.data_maintenance_lines:
                #create products
                product_tmpl_id = self.env['product.template'].create({
                    'name': vn.display_name + '-' + dm.routing_id.name,
                    'type':self.type,
                    'categ_id':dm.categ_id.id,
                    'sale_ok':False,
                    'purchase_ok':True,
                    'uom_id':self.uom_id.id,
                    'uom_po_id':self.uom_po_id.id,
                    'parent_product_tmpl_id': parent_product_tmpl_id,
                    'ref_product_tmpl_id': self.id,
                })
                
                product_id = self.env['product.product'].search([('product_tmpl_id', '=', product_tmpl_id.id)],limit=1)
                #create parent bom
                if parent_product_tmpl_id == self.id:
                    parent_bom_id = self.env['mrp.bom'].create({
                        'product_tmpl_id':self.id,
                        'product_id': vn.id,
                        'product_uom_id':self.uom_id.id,
                        'product_qty':1,
                        'type':'normal',
                    })
                    parent_bom_line = self.env['mrp.bom.line'].create({
                        'bom_id': parent_bom_id.id,
                        'product_id':product_id.id,
                        'product_qty':1,
                    })
                parent_product_tmpl_id = product_tmpl_id.id
        
        for product in self.ref_product_tmpl_ids:
            component_product_id = self.env['product.template'].search([('parent_product_tmpl_id', '=', product.id)],limit=1)
            component_id = self.env['product.product'].search([('product_tmpl_id', '=', component_product_id.id)],limit=1)
            #create bom
            if component_id:
                bom_id = self.env['mrp.bom'].create({
                    'product_tmpl_id':product.id,
                    'product_uom_id':product.uom_id.id,
                    'product_qty':1,
                    'type':'normal',
                })
                bom_line = self.env['mrp.bom.line'].create({
                    'bom_id': bom_id.id,
                    'product_id':component_id.id,
                    'product_qty':1,
                })

class ProductDataMaintenance(models.Model):
    _name = 'product.data.maintain'
    _description = 'Product Data Maintenance'
    
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, ondelete='cascade')
    routing_id = fields.Many2one('mrp.routing', string='Routing',on_delete='setnull', required=True)
    categ_id = fields.Many2one('product.category', 'Product Category', required=True, help="Select category for the current product")
    is_variant_maintenance = fields.Boolean("Is Variant", default=False)
    is_reorder_rule_maintenance = fields.Boolean("Is Reorder Rule", default=False)
    is_bom_maintenance = fields.Boolean("Is Bom", default=False)
    bom_type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('subcontract', 'Subcontracting')], 'BoM Type',
        default='normal', required=True)
    
    