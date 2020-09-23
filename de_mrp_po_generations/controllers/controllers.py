# -*- coding: utf-8 -*-
# from odoo import http


# class DeMrpPoGeneration(http.Controller):
#     @http.route('/de_mrp_po_generation/de_mrp_po_generation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_mrp_po_generation/de_mrp_po_generation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_mrp_po_generation.listing', {
#             'root': '/de_mrp_po_generation/de_mrp_po_generation',
#             'objects': http.request.env['de_mrp_po_generation.de_mrp_po_generation'].search([]),
#         })

#     @http.route('/de_mrp_po_generation/de_mrp_po_generation/objects/<model("de_mrp_po_generation.de_mrp_po_generation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_mrp_po_generation.object', {
#             'object': obj
#         })
