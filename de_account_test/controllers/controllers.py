# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountTest(http.Controller):
#     @http.route('/de_account_test/de_account_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_test/de_account_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_test.listing', {
#             'root': '/de_account_test/de_account_test',
#             'objects': http.request.env['de_account_test.de_account_test'].search([]),
#         })

#     @http.route('/de_account_test/de_account_test/objects/<model("de_account_test.de_account_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_test.object', {
#             'object': obj
#         })
