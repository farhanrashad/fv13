from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class MoBeforhandWizard(models.Model):
    _name = 'mrp.mo.beforehand'
    _description = 'Create PO from MO'

    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('job.order.sheet') or 'New'
        result = super(JobOrderSheet, self).create(vals)
        return result

    def get_sheet_lines(self):
        for rec in self:
            rec.sheet_ids.unlink()
            order_data = self.env['mrp.production'].search([('sale_id', '=', rec.sale_id.name),
                                                            '|',
                                                            '|',
                                                            ('product_id.name', '=ilike', ' %'),
                                                            ('product_id.name', '=ilike', 'Module%'),
                                                            '|',
                                                            ('product_id.name', '=ilike', '[Un-Finished]%'),
                                                            ('product_id.name', '=ilike', '[Module]%')])
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
        for line in self.sheet_ids:
            print(line.product_name)
            update_qty = line.in_house_production + line.outsource_production
            order = self.env['mrp.production'].search([('id', '=', line.mo_order_id.id)])
            order.update({
                'product_qty': line.in_house_production
            })
            stock_picking = self.env['stock.picking'].search([('origin', '=', line.mo_order_id.name),
                                                              ('picking_type_id', '=', 10)])
            print('stock', stock_picking)
            for picking in stock_picking:
                for pick_line in picking.move_ids_without_package:
                    print('qty', line.in_house_production)
                    pick_line.update({
                        'product_uom_qty': line.in_house_production * 2
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
    sale_id = fields.Many2one('sale.order',string="Ref Sale")
    mo_line_ids = fields.One2many('mrp.mo.beforehand.line','mo_id',string="Manufacturing Order")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Completed')],
        readonly=True, string='State', default='draft')
    

    
    
    
class MoBeforhandWizardLine(models.Model):
    _name = 'mrp.mo.beforehand.line'
    _description = 'Create PO from MO'
    
    active = fields.Boolean(string='Select')
    product_id = fields.Many2one('product.product',string="Product")
    product_uom_qty = fields.Float(string='Qty to consume')
    on_hand_qty = fields.Float(string="Quantity On Hand")
    forcast_qty = fields.Float(string="Forcast Quantity")
    mo_id = fields.Many2one('mrp.mo.beforehand',string="Product")    

