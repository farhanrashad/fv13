# -*- coding: utf-8 -*-
# from odoo import http


# class DeSalesEstimation(http.Controller):
#     @http.route('/de_sales_estimation/de_sales_estimation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sales_estimation/de_sales_estimation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sales_estimation.listing', {
#             'root': '/de_sales_estimation/de_sales_estimation',
#             'objects': http.request.env['de_sales_estimation.de_sales_estimation'].search([]),
#         })

#     @http.route('/de_sales_estimation/de_sales_estimation/objects/<model("de_sales_estimation.de_sales_estimation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sales_estimation.object', {
#             'object': obj
#         })
