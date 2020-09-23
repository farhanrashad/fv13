from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class MoBeforhand(models.Model):
    _name = 'mrp.mo.beforehand'
    _description = 'Create PO from MO'
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mrp.mo.beforehand') or _('New')    
        res = super(MoBeforhand,self).create(vals)
        return res

    
   

    def get_sheet_lines(self):
        for rec in self:
            rec.mo_line_ids.unlink()
            order_data = self.env['mrp.production'].search([('sale_id', '=', rec.sale_id.name),('product_id.name', '=ilike', '[Module]%')])
            data = []
            for order in order_data:
                for line in order.move_raw_ids:
                    if not '[Cut Material]' in line.product_id.name:
                        data.append((0,0,{
                                    'mo_id': self.id,
                                    'po_process': True, 
                                    'product_id': line.product_id.id,
                                    'product_uom_qty': line.product_uom_qty,
                                    'on_hand_qty':line.product_id.qty_available,
                                    'forcast_qty': line.product_id.virtual_available,
                             }))
                        
            rec.mo_line_ids = data
            
    def action_generate_po(self):
        vendor_list = []
        for line in self.mo_line_ids:
            if line.partner_id:
                vendor_list.append(line.partner_id)
            else:
                pass
        list = set(vendor_list)
        for te in list:
            product = []
            for re in self.mo_line_ids:
                if te == re.partner_id:
                    if re.po_process == True:
                        valss = {
                            'product_id': re.product_id.id,
                            'name': re.product_id.name,
                            'product_uom_qty': re.product_uom_qty,
                            'price_unit': re.product_id.standard_price,
                            'date_planned': fields.Date.today(),
                            'product_uom': re.product_id.uom_po_id.id,
                        }
                        product.append(valss)
            vals = {
                  'partner_id': te.id,
                  'date_order': fields.Date.today(),
                  'origin': self.name,
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
                for line in self.mo_line_ids:
            	    if line.po_process == True and line.partner_id==True:
                        line.update ({
                        'po_process': False,
                    	})    
                
                    
            
#     def action_quantity_vendor(self):        
            


            
    def action_approve(self):
        self.state = 'approved'

    def action_completed(self):
        self.state = 'done'

    

    name = fields.Char(
        'Reference', copy=False, readonly=True, default=lambda x: _('New'))
    date = fields.Date(string='Date', required=True)
    sale_id = fields.Many2one('sale.order',string="Ref Sale", required=True)
    partner_id = fields.Many2one('res.partner', string="Vendor")
    mo_line_ids = fields.One2many('mrp.mo.beforehand.line','mo_id',string="Manufacturing Order")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Completed')],
        readonly=True, string='State', default='draft')
    
    
    

    
    @api.onchange('partner_id')
    def onchange_partner(self):
        for line in self.mo_line_ids:
            if line.po_process == True:
                line.update ({
                        'partner_id': self.partner_id.id,
                    })  
        


    
    
    
class MoBeforhandWizardLine(models.Model):
    _name = 'mrp.mo.beforehand.line'
    _description = 'Create PO from MO'
    
    po_process = fields.Boolean(string='Select')
    product_id = fields.Many2one('product.product',string="Product")
    product_uom_qty = fields.Float(string='Qty to Required')
    on_hand_qty = fields.Float(string="Quantity On Hand")
    forcast_qty = fields.Float(string="Forcast Quantity")
    mo_id = fields.Many2one('mrp.mo.beforehand',string="Product")
    partner_id = fields.Many2one('res.partner', string="Vendor")

