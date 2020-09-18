# -*- coding: utf-8 -*-
# from odoo import http


# class DeMrpWorkorders(http.Controller):
#     @http.route('/de_mrp_workorders/de_mrp_workorders/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_mrp_workorders/de_mrp_workorders/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_mrp_workorders.listing', {
#             'root': '/de_mrp_workorders/de_mrp_workorders',
#             'objects': http.request.env['de_mrp_workorders.de_mrp_workorders'].search([]),
#         })

#     @http.route('/de_mrp_workorders/de_mrp_workorders/objects/<model("de_mrp_workorders.de_mrp_workorders"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_mrp_workorders.object', {
#             'object': obj
#         })
