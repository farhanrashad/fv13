# -*- coding: utf-8 -*-
# from odoo import http


# class DeDisciplinaryAction(http.Controller):
#     @http.route('/de_disciplinary_action/de_disciplinary_action/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_disciplinary_action/de_disciplinary_action/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_disciplinary_action.listing', {
#             'root': '/de_disciplinary_action/de_disciplinary_action',
#             'objects': http.request.env['de_disciplinary_action.de_disciplinary_action'].search([]),
#         })

#     @http.route('/de_disciplinary_action/de_disciplinary_action/objects/<model("de_disciplinary_action.de_disciplinary_action"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_disciplinary_action.object', {
#             'object': obj
#         })
