# -*- coding: utf-8 -*-
from odoo import http

# class DeAccountTaxCalculation(http.Controller):
#     @http.route('/de_account_tax_calculation/de_account_tax_calculation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_tax_calculation/de_account_tax_calculation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_tax_calculation.listing', {
#             'root': '/de_account_tax_calculation/de_account_tax_calculation',
#             'objects': http.request.env['de_account_tax_calculation.de_account_tax_calculation'].search([]),
#         })

#     @http.route('/de_account_tax_calculation/de_account_tax_calculation/objects/<model("de_account_tax_calculation.de_account_tax_calculation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_tax_calculation.object', {
#             'object': obj
#         })