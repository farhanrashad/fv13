# -*- coding: utf-8 -*-
# from odoo import http


# class DeResPartnerSecurity(http.Controller):
#     @http.route('/de_res_partner_security/de_res_partner_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_res_partner_security/de_res_partner_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_res_partner_security.listing', {
#             'root': '/de_res_partner_security/de_res_partner_security',
#             'objects': http.request.env['de_res_partner_security.de_res_partner_security'].search([]),
#         })

#     @http.route('/de_res_partner_security/de_res_partner_security/objects/<model("de_res_partner_security.de_res_partner_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_res_partner_security.object', {
#             'object': obj
#         })
