# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleIncentive(http.Controller):
#     @http.route('/de_sale_incentive/de_sale_incentive/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_incentive/de_sale_incentive/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_incentive.listing', {
#             'root': '/de_sale_incentive/de_sale_incentive',
#             'objects': http.request.env['de_sale_incentive.de_sale_incentive'].search([]),
#         })

#     @http.route('/de_sale_incentive/de_sale_incentive/objects/<model("de_sale_incentive.de_sale_incentive"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_incentive.object', {
#             'object': obj
#         })
