# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_account_test(models.Model):
#     _name = 'de_account_test.de_account_test'
#     _description = 'de_account_test.de_account_test'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
