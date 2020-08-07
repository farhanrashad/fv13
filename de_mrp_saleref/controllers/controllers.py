# -*- coding: utf-8 -*-
# from odoo import http


# class DeHrTraining(http.Controller):
#     @http.route('/de_hr_training/de_hr_training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_hr_training/de_hr_training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_hr_training.listing', {
#             'root': '/de_hr_training/de_hr_training',
#             'objects': http.request.env['de_hr_training.de_hr_training'].search([]),
#         })

#     @http.route('/de_hr_training/de_hr_training/objects/<model("de_hr_training.de_hr_training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_hr_training.object', {
#             'object': obj
#         })
