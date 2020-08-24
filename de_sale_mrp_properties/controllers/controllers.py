# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleMrpProperties(http.Controller):
#     @http.route('/de_sale_mrp_properties/de_sale_mrp_properties/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_mrp_properties/de_sale_mrp_properties/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_mrp_properties.listing', {
#             'root': '/de_sale_mrp_properties/de_sale_mrp_properties',
#             'objects': http.request.env['de_sale_mrp_properties.de_sale_mrp_properties'].search([]),
#         })

#     @http.route('/de_sale_mrp_properties/de_sale_mrp_properties/objects/<model("de_sale_mrp_properties.de_sale_mrp_properties"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_mrp_properties.object', {
#             'object': obj
#         })
