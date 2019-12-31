# -*- coding: utf-8 -*-
# from odoo import http


# class DeEquipmentMaintenance(http.Controller):
#     @http.route('/de_equipment_maintenance/de_equipment_maintenance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_equipment_maintenance/de_equipment_maintenance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_equipment_maintenance.listing', {
#             'root': '/de_equipment_maintenance/de_equipment_maintenance',
#             'objects': http.request.env['de_equipment_maintenance.de_equipment_maintenance'].search([]),
#         })

#     @http.route('/de_equipment_maintenance/de_equipment_maintenance/objects/<model("de_equipment_maintenance.de_equipment_maintenance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_equipment_maintenance.object', {
#             'object': obj
#         })
