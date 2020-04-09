# -*- coding: utf-8 -*-
# from odoo import http


# class DeSubcontractQuantity(http.Controller):
#     @http.route('/de_subcontract_quantity/de_subcontract_quantity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_subcontract_quantity/de_subcontract_quantity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_subcontract_quantity.listing', {
#             'root': '/de_subcontract_quantity/de_subcontract_quantity',
#             'objects': http.request.env['de_subcontract_quantity.de_subcontract_quantity'].search([]),
#         })

#     @http.route('/de_subcontract_quantity/de_subcontract_quantity/objects/<model("de_subcontract_quantity.de_subcontract_quantity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_subcontract_quantity.object', {
#             'object': obj
#         })
