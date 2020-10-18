# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from collections import defaultdict
from odoo.exceptions import UserError


class PurchaseOrderExt(models.Model):
    _inherit = 'purchase.order'

    jo_sheet_reference = fields.Char(string='Reference')


class MrpProductionSale(models.Model):
    _inherit = 'mrp.production'

    sale_order = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    # sale_id = fields.Char(string='Ref Sale')


class JobOrderSheet(models.Model):
    _name = 'job.order.sheet'
    _description = 'Job Order Sheet'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('job.order.sheet') or 'New'
        result = super(JobOrderSheet, self).create(vals)
        return result

    def get_sheet_lines(self):
        for rec in self:
            rec.sheet_ids.unlink()
            picking_type = self.env['stock.picking.type'].search([('name', '=', 'Floor - Receiving')], limit=1)
            print('picking', picking_type)
            order_data = self.env['mrp.production'].search([('sale_id', '=', rec.sale_order_id.name),
                                                            ('product_id.name', 'ilike', '[Un-Finished]%'),
                                                            ('picking_type_id', '=', picking_type.id)])
            print('dtaa', order_data)
            for order in order_data:
                rec.sheet_ids |= rec.sheet_ids.new({
                    'mo_order_id': order.id,
                    'product_id': order.product_id.id,
                    'product_quantity': order.product_qty,
                })
            rec.write({
                'progress': 'done',
            })

    def action_approve(self):
        self.state = 'approved'

    def action_completed(self):
        self.state = 'done'

    def action_quantity_update(self):
        pickings = []
        picking_doc = self.env['stock.picking.type'].search([('name', 'in',
                                                              ['Pick Components from Supply',
                                                               'Supply Finished Product'])])
        print('doc', picking_doc)
        for pick in picking_doc:
            pickings.append(pick.id)
        for line in self.sheet_ids:
            print(line.product_name)
            update_qty = line.in_house_production + line.outsource_production
            order = self.env['mrp.production'].search([('id', '=', line.mo_order_id.id)])
            order.update({
                'product_qty': line.in_house_production
            })
            stock_picking = self.env['stock.picking'].search([('origin', '=', line.mo_order_id.name),
                                                              ('picking_type_id', 'in', pickings)])
            print('stock', stock_picking)
            for picking in stock_picking:
                for pick_line in picking.move_ids_without_package:
                    print('qty', line.in_house_production)
                    pick_line.update({
                        'product_uom_qty': line.in_house_production
                    })
            for qty in order.move_raw_ids:
                qty.update({
                    'product_uom_qty': line.in_house_production
                })

    def action_generate_po(self):
        for line in self.sheet_ids:
            if line.outsource_production > 0:
                supplier_line = {
                    'product_id': line.product_id.id,
                    'name': 'Product',
                    'product_qty': line.outsource_production,
                    'price_unit': line.product_id.list_price,
                    'order_id': self.id,
                    'date_planned': fields.Date.today(),
                    'product_uom': line.product_id.uom_id.id,
                }
                b_prod = self.env['product.product'].search([('id', '=', line.product_id.id)])
                b_prod_line = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', b_prod.id)], limit=1)
                print(b_prod_line.name.name)
                self.env['purchase.order'].create({
                    'partner_id': line.vendor_id.id,
                    'jo_sheet_reference': self.name,
                    # 'sale_order_ref': rec.job_order_id.sale_order_id.name,
                    'date_order': fields.Date.today(),
                    'order_line': [(0, 0, supplier_line)],
                })
                self.write({
                    'po_created': True
                })

    name = fields.Char(
        'Reference', copy=False, readonly=True, default=lambda x: _('New'))
    date = fields.Date(string='Date', required=True)
    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Completed')],
        readonly=True, string='State', default='draft')
    progress = fields.Selection([
        ('in_progress', 'In Progress'),
        ('done', 'Done')], 'Progress',
        default='in_progress')
    po_created = fields.Boolean(string='PO Created')
    space = fields.Char(default=" ", readonly=True)
    sheet_ids = fields.One2many(comodel_name='job.order.sheet.line', inverse_name='sheet_id')


class JobOrderSheetLine(models.Model):
    _name = 'job.order.sheet.line'
    _description = 'Material Planning'

    def update_product_quantity(self):
        for rec in self:
            self.write({
                'product_quantity': rec.update_quantity,
            })
            order = self.env['mrp.production'].search([('id', '=', rec.mo_order_id.id)])
            order.update({
                'product_qty': rec.update_quantity,
            })

    sheet_id = fields.Many2one(comodel_name='job.order.sheet')
    mo_order_id = fields.Many2one(comodel_name='mrp.production', string='Reference', required=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    product_name = fields.Char(string='Product Name', related='product_id.name')
    product_quantity = fields.Float(string='Quantity')
    in_house_production = fields.Float(string='InHouse Production')
    outsource_production = fields.Float(string='Outsource Production')
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor')
