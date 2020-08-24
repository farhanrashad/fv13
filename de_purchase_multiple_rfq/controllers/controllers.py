# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseMultipleRfq(http.Controller):
#     @http.route('/de_purchase_multiple_rfq/de_purchase_multiple_rfq/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_multiple_rfq/de_purchase_multiple_rfq/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_multiple_rfq.listing', {
#             'root': '/de_purchase_multiple_rfq/de_purchase_multiple_rfq',
#             'objects': http.request.env['de_purchase_multiple_rfq.de_purchase_multiple_rfq'].search([]),
#         })

#     @http.route('/de_purchase_multiple_rfq/de_purchase_multiple_rfq/objects/<model("de_purchase_multiple_rfq.de_purchase_multiple_rfq"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_multiple_rfq.object', {
#             'object': obj
#         })
