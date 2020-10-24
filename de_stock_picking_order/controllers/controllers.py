# -*- coding: utf-8 -*-
# from odoo import http


# class DeStockPickingOrder(http.Controller):
#     @http.route('/de_stock_picking_order/de_stock_picking_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_picking_order/de_stock_picking_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_picking_order.listing', {
#             'root': '/de_stock_picking_order/de_stock_picking_order',
#             'objects': http.request.env['de_stock_picking_order.de_stock_picking_order'].search([]),
#         })

#     @http.route('/de_stock_picking_order/de_stock_picking_order/objects/<model("de_stock_picking_order.de_stock_picking_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_picking_order.object', {
#             'object': obj
#         })
