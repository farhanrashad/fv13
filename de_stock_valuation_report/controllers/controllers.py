# -*- coding: utf-8 -*-
from odoo import http

# class DeStockReports(http.Controller):
#     @http.route('/de_stock_reports/de_stock_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_reports/de_stock_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_reports.listing', {
#             'root': '/de_stock_reports/de_stock_reports',
#             'objects': http.request.env['de_stock_reports.de_stock_reports'].search([]),
#         })

#     @http.route('/de_stock_reports/de_stock_reports/objects/<model("de_stock_reports.de_stock_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_reports.object', {
#             'object': obj
#         })