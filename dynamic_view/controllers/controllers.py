# -*- coding: utf-8 -*-
from openerp import http

# class /users/moylop260/odoo/dynamicView(http.Controller):
#     @http.route('//users/moylop260/odoo/dynamic_view//users/moylop260/odoo/dynamic_view/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//users/moylop260/odoo/dynamic_view//users/moylop260/odoo/dynamic_view/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/users/moylop260/odoo/dynamic_view.listing', {
#             'root': '//users/moylop260/odoo/dynamic_view//users/moylop260/odoo/dynamic_view',
#             'objects': http.request.env['/users/moylop260/odoo/dynamic_view./users/moylop260/odoo/dynamic_view'].search([]),
#         })

#     @http.route('//users/moylop260/odoo/dynamic_view//users/moylop260/odoo/dynamic_view/objects/<model("/users/moylop260/odoo/dynamic_view./users/moylop260/odoo/dynamic_view"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/users/moylop260/odoo/dynamic_view.object', {
#             'object': obj
#         })