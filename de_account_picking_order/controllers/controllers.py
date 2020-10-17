# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountPickingOrder(http.Controller):
#     @http.route('/de_account_picking_order/de_account_picking_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_picking_order/de_account_picking_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_picking_order.listing', {
#             'root': '/de_account_picking_order/de_account_picking_order',
#             'objects': http.request.env['de_account_picking_order.de_account_picking_order'].search([]),
#         })

#     @http.route('/de_account_picking_order/de_account_picking_order/objects/<model("de_account_picking_order.de_account_picking_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_picking_order.object', {
#             'object': obj
#         })
