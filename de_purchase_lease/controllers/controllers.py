# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseLease(http.Controller):
#     @http.route('/de_purchase_lease/de_purchase_lease/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_lease/de_purchase_lease/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_lease.listing', {
#             'root': '/de_purchase_lease/de_purchase_lease',
#             'objects': http.request.env['de_purchase_lease.de_purchase_lease'].search([]),
#         })

#     @http.route('/de_purchase_lease/de_purchase_lease/objects/<model("de_purchase_lease.de_purchase_lease"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_lease.object', {
#             'object': obj
#         })
