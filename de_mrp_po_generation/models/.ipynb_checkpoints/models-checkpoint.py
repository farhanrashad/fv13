from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class MoBeforhand(models.Model):
    _name = 'mrp.mo.beforehand'
    _description = 'Create PO from MO'

    
   

    def get_sheet_lines(self):
        for rec in self:
            rec.mo_line_ids.unlink()
            order_data = self.env['mrp.production'].search([('sale_id', '=', rec.sale_id.name),('product_id.name', '=ilike', '[Module]%')])
            for order in order_data:
                data = []
                for line in order.move_raw_ids:
#                     .search([('product_id.name', '=ilike', not '[Cut Material]%'),])
#                 for line in order_line:
                    
#                 for line    
#                     for product in line:
#                         product_exist = product.search([('product_id.name', '=ilike', '[Printed Finger]%'),])
#                     if  product_exist:
                  data.append((0,0,{
                                    'mo_id': self.id,
                                    'po_process': True, 
                                    'product_id': line.product_id.id,
                                    'product_uom_qty': line.product_uom_qty,
                                    'on_hand_qty':line.product_id.qty_available,
                                    'forcast_qty': line.product_id.virtual_available,
                             }))
                        
            rec.mo_line_ids = data
            
    def action_quantity_vendor(self):        
            


            
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
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mrp.mo.beforehand') or _('New')            
        res = super(MoBeforhand,self).create(vals)
        return res
    

    
    
    
class MoBeforhandWizardLine(models.Model):
    _name = 'mrp.mo.beforehand.line'
    _description = 'Create PO from MO'
    
    po_process = fields.Boolean(string='Select')
    product_id = fields.Many2one('product.product',string="Product")
    product_uom_qty = fields.Float(string='Qty to consume')
    on_hand_qty = fields.Float(string="Quantity On Hand")
    forcast_qty = fields.Float(string="Forcast Quantity")
    mo_id = fields.Many2one('mrp.mo.beforehand',string="Product")
    partner_id = fields.Many2one('purchase.order', string="Vendor")

