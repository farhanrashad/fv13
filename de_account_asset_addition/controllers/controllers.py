# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountAssetAddition(http.Controller):
#     @http.route('/de_account_asset_addition/de_account_asset_addition/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_asset_addition/de_account_asset_addition/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_asset_addition.listing', {
#             'root': '/de_account_asset_addition/de_account_asset_addition',
#             'objects': http.request.env['de_account_asset_addition.de_account_asset_addition'].search([]),
#         })

#     @http.route('/de_account_asset_addition/de_account_asset_addition/objects/<model("de_account_asset_addition.de_account_asset_addition"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_asset_addition.object', {
#             'object': obj
#         })
