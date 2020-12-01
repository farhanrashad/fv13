# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_charge = fields.Boolean(string='Is Charge', store=True)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    
    def get_bill_count(self):
        count = self.env['account.move'].search_count([('invoice_origin', '=', self.name)])
        self.bill_count = count
        
    bill_count = fields.Integer(string='Bill Count', compute='get_bill_count')
    
    
    def action_vendor_bill(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
#             'multi': False,
            'name': 'Vendor Bill',
            'domain': [('invoice_origin','=', self.name)],
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }
    
    
    def button_generate_bill(self):
        vendor_list = []
        for line in self.cost_lines:
            if line.partner_id and line.is_billed == False:
                vendor_list.append(line.partner_id)
            else:
                pass
        list = set(vendor_list)
        for partner in list:
            product_list = []
            for line in self.cost_lines:
                if partner == line.partner_id:
                    if line.is_billed == False:
                        product_list.append((0,0, {
                            'product_id': line.product_id.id,
                            'name': line.product_id.name,
                            'account_id': line.account_id.id,
                            'quantity': line.quantity, 
                            'price_unit': line.product_id.standard_price,
                            'partner_id': line.partner_id.id,
                            'product_uom_id': line.product_id.uom_po_id.id,
                        }))
#                         product_list.append(valss)
            vals = {
                  'partner_id': partner.id,
                  'journal_id': self.journal_id.id,
                  'invoice_date': fields.Date.today(),
                  'type': 'in_invoice',
                  'invoice_origin': self.name,
                  'invoice_line_ids': product_list   
                    }
            move = self.env['account.move'].create(vals)     
        for line in self.cost_lines:
            if line.is_billed == False and line.partner_id:
                line.update ({
#                    'po_process': False,
                    'is_billed': True,
                  	})
                
    def _get_default_journal(self):
        return self.env['account.journal'].search([
            ('type', '=', 'purchase'),],
            limit=1).id            
    
    credit_account_id = fields.Many2one('account.account', string='Credit Account')    
    journal_id = fields.Many2one('account.journal', string='Journal', default=_get_default_journal)
    cost_lines = fields.One2many('mrp.production.direct.cost', 'production_id' ,string='Direct Cost Lines')    
    
    
class MrpCost(models.Model):
    _name = 'mrp.production.direct.cost'
    _description = 'This Production Order Cost'
    
    def _get_default_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'STOCK INTERIM (RECEIVED)'),],
            limit=1).id
    

    product_id = fields.Many2one('product.product',string='Product', domain="[('type', '=', 'service')]")
    account_id = fields.Many2one('account.account', string='Account', default=_get_default_account)
    quantity = fields.Float(string="Quantity")
    production_id = fields.Many2one('mrp.production', string="Manufacturing Order")
    is_charge = fields.Boolean(related='product_id.is_charge')
    standard_price = fields.Float(related='product_id.standard_price', readonly=False)
    is_billed = fields.Boolean(string='Billed', readonly=True)
    partner_id = fields.Many2one('res.partner', related='product_id.seller_ids.name',readonly=False)
    

