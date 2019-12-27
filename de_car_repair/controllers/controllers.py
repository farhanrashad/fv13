# -*- coding: utf-8 -*-
# from odoo import http


# class DeCarRepair(http.Controller):
#     @http.route('/de_car_repair/de_car_repair/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_car_repair/de_car_repair/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_car_repair.listing', {
#             'root': '/de_car_repair/de_car_repair',
#             'objects': http.request.env['de_car_repair.de_car_repair'].search([]),
#         })

#     @http.route('/de_car_repair/de_car_repair/objects/<model("de_car_repair.de_car_repair"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_car_repair.object', {
#             'object': obj
#         })
