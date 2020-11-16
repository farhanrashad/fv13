# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    
class AccountJournal(models.Model):
    _inherit = 'account.move.line'
    
class AccountJournal(models.Model):
    _inherit = 'account.journal'    

class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    @api.model
    def _get_default_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Cost of Goods Sold'),],
            limit=1).id
    
    debit_account_id = fields.Many2one('account.account', string='Issuance Account', default = _get_default_account)


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    @api.model
    def _get_default_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Cost of Goods Sold'),],
            limit=1).id
    
    account_id = fields.Many2one('account.account', string='Account',
          default = _get_default_account )
    price_unit = fields.Float(related='product_id.standard_price')
    price_subtotal = fields.Monetary(compute='_compute_amount_t', string='Subtotal')
    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account',
        readonly=False, copy=False, check_company=True, 
        help="The analytic account related to a sales order.")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    currency_id = fields.Many2one('res.currency', 'Currency')
    company_id = fields.Many2one('res.company', store=True, string='Company', readonly=False)
    

   

    
    @api.depends('price_subtotal','price_unit', 'product_uom_qty')    
    def _compute_amount_t(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.product_uom_qty     
    
                

    

   
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    
    def button_validate(self):
        if self.picking_type_id.name == 'General trasnfer':
            for line in self.move_ids_without_package:
    #             stock_quant = self.env['stock.quant'].search([('product_id','=',line.product_id.id),('location_id','=',line.location_id.id)])
    #             for stock in stock_quant:                
                if line.product_id.qty_available >= line.quantity_done:
                    pass
                else:
                    raise UserError(_('Stock Quantity less than Demand Quantity for Product: ' + ' ' + line.product_id.name + ' ' + 'At Location' + ' '+ self.location_id.name ))
        
        res = super(StockPicking, self).button_validate()
        if self.picking_type_id.name == 'General trasnfer':
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            move_dict = {
                  'name': self.name,
                'journal_id': self.journal_id.id,
                  'date': self.scheduled_date,
                  'state': 'draft',
                       }
            for oline in self.move_ids_without_package:
                debit_line = (0, 0, {
                        'name': self.name +":"+ oline.product_id.name,
                    'debit': abs(oline.price_subtotal),
                        'credit': 0.0,
                        #'analytic_account_id': oline.analytic_account_id.id,
                        #'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                        'account_id': oline.product_id.categ_id.debit_account_id.id,
                })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']            
                credit_line = (0, 0, {
                          'name': self.name +":"+ oline.product_id.name,
                          'debit': 0.0,
                          'credit': abs(oline.price_subtotal),
                          'account_id': oline.product_id.categ_id.property_stock_valuation_account_id.id,
                                  })
                line_ids.append(credit_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)

        return res
        
    @api.model
    def _get_default_debit_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Cost of Goods Sold'),],
            limit=1).id
        
#     @api.model
#     def _get_default_credit_account(self):
#         return self.env['account.account'].search([
#             ('name', '=', 'Stock Valuation Account'),],
#             limit=1).id
        
    @api.model
    def _get_default_journal(self):
        return self.env['account.journal'].search([
            ('name', '=', 'Miscellaneous Operations'),],
            limit=1).id
        

        
    def action_view_test(self):
        self.ensure_one()
        return {
         'type': 'ir.actions.act_window',
         'binding_type': 'object',
         'domain': [('name', '=', self.name)],
         'multi': False,
         'name': 'Tasks',
         'target': 'current',
         'res_model': 'account.move',
         'view_mode': 'tree,form',
        }
        

        
    def get_bill_count(self):
        count = self.env['account.move'].search_count([('name', '=', self.name)])
        self.bill_count = count
        
        
    bill_count = fields.Integer(string='Sub Task', compute='get_bill_count')
#     credit_account_id = fields.Many2one('account.account', string='Credit Account', default = _get_default_credit_account)
    journal_id = fields.Many2one('account.journal', string='Journal', default = _get_default_journal)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    currency_id = fields.Many2one('res.currency', 'Currency')
    record_expense = fields.Boolean(string='Expense')
        
        



    @api.depends('move_ids_without_package.price_subtotal')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.move_ids_without_package:
                amount_untaxed += line.price_subtotal 
        order.update({
            'amount_total': amount_untaxed
            })
            
        
    def action_record_expense(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        move_dict = {
              'name': self.name,
              'journal_id': self.journal_id.id,
              'date': self.scheduled_date,
              'state': 'draft',
                   }
        for oline in self.move_ids_without_package:
            debit_line = (0, 0, {
                    'name': self.name +":"+ oline.product_id.name,
                    'debit': abs(oline.price_subtotal),
                    'credit': 0.0,
                    'analytic_account_id': oline.analytic_account_id.id,
                    'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                    'account_id': oline.product_id.categ_id.debit_account_id.id,
                         })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']            
            credit_line = (0, 0, {
                  'name': self.name +":"+ oline.product_id.name,
                  'debit': 0.0,
                  'credit': abs(oline.price_subtotal),
                  'account_id': oline.product_id.categ_id.property_stock_valuation_account_id.id,
                          })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

        move_dict['line_ids'] = line_ids
        move = self.env['account.move'].create(move_dict)



        

