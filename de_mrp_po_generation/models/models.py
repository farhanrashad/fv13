from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class MoBeforhand(models.Model):
    _name = 'mrp.mo.beforehand'
    _description = 'Create PO from MO'

    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('mrp.mo.beforehand') or 'New'
        result = super(MoBeforhand, self).create(vals)
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

