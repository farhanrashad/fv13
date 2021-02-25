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
    _inherit = 'account.invoice'

    agent_id = fields.Many2one(related='partner_id.agent_id')
    commission_rate = fields.Float(string='Commission Rate')
    commission = fields.Float(string='Commission', compute='compute_commission')
    
    @api.onchange('invoice_line_ids.quantity')
    def compute_commission(self):
        for record in self:
            total_quantity = 0
            for line in record.invoice_line_ids:
                if line.package_id.shipping_grade == 'fresh':
                    total_quantity = total_quantity + line.quantity
            
            record.commission = total_quantity * record.commission_rate
