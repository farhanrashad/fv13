# -*- coding: utf-8 -*-
# from odoo import http


# class DePayslipPayment(http.Controller):
#     @http.route('/de_payslip_payment/de_payslip_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payslip_payment/de_payslip_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payslip_payment.listing', {
#             'root': '/de_payslip_payment/de_payslip_payment',
#             'objects': http.request.env['de_payslip_payment.de_payslip_payment'].search([]),
#         })

#     @http.route('/de_payslip_payment/de_payslip_payment/objects/<model("de_payslip_payment.de_payslip_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payslip_payment.object', {
#             'object': obj
#         })
