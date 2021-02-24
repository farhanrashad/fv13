from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_agent = fields.Boolean(string='Is a Agent')
    agent_id = fields.Many2one('res.partner', string='Agent', domain="[('is_agent','=',True),('id','!=',id)]")
    

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one(related='partner_id.agent_id')
    

class AccountInvoiceInherit(models.Model):
    _inherit = 'account.move'
    
    
    @api.model
    def action_create_bill(self):
#         agent_list = []
#         for invoice in self:
#             if invoice.agent_id and invoice.commission_settled == False:
#                 agent_list.append(invoice.agent_id)
                
#         list = set(agent_list)
#         product_list = []
#         for agent in list:
#             total_commission_amount = 0
#             for agent_invoice in self:
#                 if  agent_invoice.agent_id.id ==  agent.id  and agent_invoice.commission_settled == False:
#                     total_commission_amount = total_commission_amount + agent_invoice.commission  
                    
# #                 invoice.update({
# #                 'commission_settled': True,
# #                 })  
        commission_list = []
        commission_list.append((0,0, {
                        'name': 'Commission Bill',
                        'account_id': 13,
                        'quantity': 1, 
                        'price_unit': 20,
                        'partner_id': 4438,
                            }))

        vals = {
                'partner_id': 4438,
                'journal_id': 2,
                'invoice_date': fields.Date.today(),
                'type': 'in_invoice',
                'invoice_origin': 'Commission',
                'amount_total': 100, 
                'invoice_line_ids': commission_list,   
                    }
        move = self.env['account.move'].create(vals)
        

    agent_id = fields.Many2one(related='partner_id.agent_id')
    commission_rate = fields.Float(string='Commission Rate')
    commission = fields.Float(string='Commission', compute='compute_commission')
    commission_settled = fields.Boolean(string="Commission Settled", readonly=True)
    
    @api.onchange('invoice_line_ids.quantity')
    def compute_commission(self):
        for record in self:
            total_quantity = 0
            total_commission_rate = 0
            for line in record.invoice_line_ids:
#                 if line.package_id.shipping_grade == 'fresh':
                total_quantity = total_quantity + line.quantity
                total_commission_rate = total_commission_rate + line.commission_rate  
            record.commission = total_quantity * total_commission_rate
            
            
class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    commission_rate = fields.Float(string='Commission Rate')            
