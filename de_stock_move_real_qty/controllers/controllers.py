# -*- coding: utf-8 -*-
# from odoo import http


# class DeStockMoveRealQty(http.Controller):
#     @http.route('/de_stock_move_real_qty/de_stock_move_real_qty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_move_real_qty/de_stock_move_real_qty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_move_real_qty.listing', {
#             'root': '/de_stock_move_real_qty/de_stock_move_real_qty',
#             'objects': http.request.env['de_stock_move_real_qty.de_stock_move_real_qty'].search([]),
#         })

#     @http.route('/de_stock_move_real_qty/de_stock_move_real_qty/objects/<model("de_stock_move_real_qty.de_stock_move_real_qty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_move_real_qty.object', {
#             'object': obj
#         })
