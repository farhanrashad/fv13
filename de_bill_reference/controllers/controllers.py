# -*- coding: utf-8 -*-
# from odoo import http


# class DeBillReference(http.Controller):
#     @http.route('/de_bill_reference/de_bill_reference/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_bill_reference/de_bill_reference/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_bill_reference.listing', {
#             'root': '/de_bill_reference/de_bill_reference',
#             'objects': http.request.env['de_bill_reference.de_bill_reference'].search([]),
#         })

#     @http.route('/de_bill_reference/de_bill_reference/objects/<model("de_bill_reference.de_bill_reference"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_bill_reference.object', {
#             'object': obj
#         })
