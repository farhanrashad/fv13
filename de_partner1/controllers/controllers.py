# -*- coding: utf-8 -*-
# from odoo import http


# class DePartner1(http.Controller):
#     @http.route('/de_partner1/de_partner1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_partner1/de_partner1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_partner1.listing', {
#             'root': '/de_partner1/de_partner1',
#             'objects': http.request.env['de_partner1.de_partner1'].search([]),
#         })

#     @http.route('/de_partner1/de_partner1/objects/<model("de_partner1.de_partner1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_partner1.object', {
#             'object': obj
#         })
