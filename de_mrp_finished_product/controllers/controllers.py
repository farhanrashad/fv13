# -*- coding: utf-8 -*-
# from odoo import http


# class DeMrpFinishedProduct(http.Controller):
#     @http.route('/de_mrp_finished_product/de_mrp_finished_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_mrp_finished_product/de_mrp_finished_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_mrp_finished_product.listing', {
#             'root': '/de_mrp_finished_product/de_mrp_finished_product',
#             'objects': http.request.env['de_mrp_finished_product.de_mrp_finished_product'].search([]),
#         })

#     @http.route('/de_mrp_finished_product/de_mrp_finished_product/objects/<model("de_mrp_finished_product.de_mrp_finished_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_mrp_finished_product.object', {
#             'object': obj
#         })
