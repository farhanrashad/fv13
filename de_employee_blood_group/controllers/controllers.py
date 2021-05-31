# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeBloodGroup(http.Controller):
#     @http.route('/de_employee_blood_group/de_employee_blood_group/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_blood_group/de_employee_blood_group/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_blood_group.listing', {
#             'root': '/de_employee_blood_group/de_employee_blood_group',
#             'objects': http.request.env['de_employee_blood_group.de_employee_blood_group'].search([]),
#         })

#     @http.route('/de_employee_blood_group/de_employee_blood_group/objects/<model("de_employee_blood_group.de_employee_blood_group"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_blood_group.object', {
#             'object': obj
#         })
