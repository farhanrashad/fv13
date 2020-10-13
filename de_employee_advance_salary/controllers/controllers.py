# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeAdvanceSalary(http.Controller):
#     @http.route('/de_employee_advance_salary/de_employee_advance_salary/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_advance_salary/de_employee_advance_salary/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_advance_salary.listing', {
#             'root': '/de_employee_advance_salary/de_employee_advance_salary',
#             'objects': http.request.env['de_employee_advance_salary.de_employee_advance_salary'].search([]),
#         })

#     @http.route('/de_employee_advance_salary/de_employee_advance_salary/objects/<model("de_employee_advance_salary.de_employee_advance_salary"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_advance_salary.object', {
#             'object': obj
#         })
