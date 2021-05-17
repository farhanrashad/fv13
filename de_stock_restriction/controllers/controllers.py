# -*- coding: utf-8 -*-
from odoo import http

# class DeStockRestriction(http.Controller):
#     @http.route('/de_stock_restriction/de_stock_restriction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_restriction/de_stock_restriction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_restriction.listing', {
#             'root': '/de_stock_restriction/de_stock_restriction',
#             'objects': http.request.env['de_stock_restriction.de_stock_restriction'].search([]),
#         })

#     @http.route('/de_stock_restriction/de_stock_restriction/objects/<model("de_stock_restriction.de_stock_restriction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_restriction.object', {
#             'object': obj
#         })