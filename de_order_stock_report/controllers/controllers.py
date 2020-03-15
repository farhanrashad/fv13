# -*- coding: utf-8 -*-
# from odoo import http


# class DeOrderProductionMovement(http.Controller):
#     @http.route('/de_order_production_movement/de_order_production_movement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_order_production_movement/de_order_production_movement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_order_production_movement.listing', {
#             'root': '/de_order_production_movement/de_order_production_movement',
#             'objects': http.request.env['de_order_production_movement.de_order_production_movement'].search([]),
#         })

#     @http.route('/de_order_production_movement/de_order_production_movement/objects/<model("de_order_production_movement.de_order_production_movement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_order_production_movement.object', {
#             'object': obj
#         })
