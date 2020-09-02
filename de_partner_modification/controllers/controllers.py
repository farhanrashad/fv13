# -*- coding: utf-8 -*-
# from odoo import http


# class DePartnerModification(http.Controller):
#     @http.route('/de_partner_modification/de_partner_modification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_partner_modification/de_partner_modification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_partner_modification.listing', {
#             'root': '/de_partner_modification/de_partner_modification',
#             'objects': http.request.env['de_partner_modification.de_partner_modification'].search([]),
#         })

#     @http.route('/de_partner_modification/de_partner_modification/objects/<model("de_partner_modification.de_partner_modification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_partner_modification.object', {
#             'object': obj
#         })
