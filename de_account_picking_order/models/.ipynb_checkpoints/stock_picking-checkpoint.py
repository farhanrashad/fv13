# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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
        
    @api.model
    def _get_default_debit_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Cost of Goods Sold'),],
            limit=1).id
        
    @api.model
    def _get_default_credit_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Stock Valuation Account'),],
            limit=1).id
        
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
    account_id = fields.Many2one('account.account', string='Credit Account')
    credit_account_id = fields.Many2one('account.account', string='Credit Account', default = _get_default_credit_account)
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
                        #step2:debit side entry
        for oline in self.move_ids_without_package:
            debit_line = (0, 0, {
    #                  	'move_id': move.id,
                    'name': self.name +":"+ oline.product_id.name,
                    'debit': abs(oline.price_subtotal),
                    'credit': 0.0,
                    'analytic_account_id': oline.analytic_account_id.id,
                    'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                    'account_id': oline.account_id.id,
                         })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                #step3:credit side entry
        credit_line = (0, 0, {
                  'name': self.name,
                  'debit': 0.0,
                  'credit': abs(self.amount_total),
                  'account_id': self.credit_account_id.id,
                          })
        line_ids.append(credit_line)
        credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

        move_dict['line_ids'] = line_ids
        move = self.env['account.move'].create(move_dict)



        

