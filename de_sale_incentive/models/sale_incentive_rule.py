# -*- coding: utf-8 -*-



from odoo import api, fields, models, _
from odoo.exceptions import UserError

class de_sale_incentive(models.Model):
    _name = 'sale.incentive.rule'
    _description = 'this table is relevent to sale incentive rules'

    name = fields.Char(string='name')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    incentive_line_ids = fields.One2many('sale.incentive.rule.line', 'incentive_id' ,string='Incentive')

class SaleIncentiveLine(models.Model):
    _name = 'sale.incentive.rule.line'
    _description = 'this table is relevent to sale incentive rules line'

    employee_id = fields.Many2one('hr.employee',string='Employee')
    incentive_id = fields.Many2one('sale.incentive.rule', string='Incentive')
    percentage = fields.Float(string='Percentage')
