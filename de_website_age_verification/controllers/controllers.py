# -*- coding: utf-8 -*-
from odoo import http

# class DeAgeVerfication(http.Controller):
#     @http.route('/de_age_verfication/de_age_verfication/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_age_verfication/de_age_verfication/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_age_verfication.listing', {
#             'root': '/de_age_verfication/de_age_verfication',
#             'objects': http.request.env['de_age_verfication.de_age_verfication'].search([]),
#         })

#     @http.route('/de_age_verfication/de_age_verfication/objects/<model("de_age_verfication.de_age_verfication"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_age_verfication.object', {
#             'object': obj
#         })