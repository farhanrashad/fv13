# -*- coding: utf-8 -*-
# from odoo import http


# class DeStockMultiUom(http.Controller):
#     @http.route('/de_stock_multi_uom/de_stock_multi_uom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_multi_uom/de_stock_multi_uom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_multi_uom.listing', {
#             'root': '/de_stock_multi_uom/de_stock_multi_uom',
#             'objects': http.request.env['de_stock_multi_uom.de_stock_multi_uom'].search([]),
#         })

#     @http.route('/de_stock_multi_uom/de_stock_multi_uom/objects/<model("de_stock_multi_uom.de_stock_multi_uom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_multi_uom.object', {
#             'object': obj
#         })
