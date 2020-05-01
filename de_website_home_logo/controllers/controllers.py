# -*- coding: utf-8 -*-
# from odoo import http


# class DeWebsiteSecondaryLogo(http.Controller):
#     @http.route('/de_website_secondary_logo/de_website_secondary_logo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_website_secondary_logo/de_website_secondary_logo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_website_secondary_logo.listing', {
#             'root': '/de_website_secondary_logo/de_website_secondary_logo',
#             'objects': http.request.env['de_website_secondary_logo.de_website_secondary_logo'].search([]),
#         })

#     @http.route('/de_website_secondary_logo/de_website_secondary_logo/objects/<model("de_website_secondary_logo.de_website_secondary_logo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_website_secondary_logo.object', {
#             'object': obj
#         })
