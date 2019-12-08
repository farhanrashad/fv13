# -*- coding: utf-8 -*-
# from odoo import http


# class DeOrderApproval(http.Controller):
#     @http.route('/de_order_approval/de_order_approval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_order_approval/de_order_approval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_order_approval.listing', {
#             'root': '/de_order_approval/de_order_approval',
#             'objects': http.request.env['de_order_approval.de_order_approval'].search([]),
#         })

#     @http.route('/de_order_approval/de_order_approval/objects/<model("de_order_approval.de_order_approval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_order_approval.object', {
#             'object': obj
#         })
