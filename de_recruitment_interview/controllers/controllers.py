# -*- coding: utf-8 -*-
# from odoo import http


# class DeRecruitmentInterview(http.Controller):
#     @http.route('/de_recruitment_interview/de_recruitment_interview/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_recruitment_interview/de_recruitment_interview/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_recruitment_interview.listing', {
#             'root': '/de_recruitment_interview/de_recruitment_interview',
#             'objects': http.request.env['de_recruitment_interview.de_recruitment_interview'].search([]),
#         })

#     @http.route('/de_recruitment_interview/de_recruitment_interview/objects/<model("de_recruitment_interview.de_recruitment_interview"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_recruitment_interview.object', {
#             'object': obj
#         })
