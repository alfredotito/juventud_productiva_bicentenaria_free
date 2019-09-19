# -*- coding: utf-8 -*-
from odoo import http

# class ResolvedQueries(http.Controller):
#     @http.route('/resolved_queries/resolved_queries/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/resolved_queries/resolved_queries/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('resolved_queries.listing', {
#             'root': '/resolved_queries/resolved_queries',
#             'objects': http.request.env['resolved_queries.resolved_queries'].search([]),
#         })

#     @http.route('/resolved_queries/resolved_queries/objects/<model("resolved_queries.resolved_queries"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('resolved_queries.object', {
#             'object': obj
#         })