# -*- coding: utf-8 -*-
# from odoo import http


# class Checklist(http.Controller):
#     @http.route('/checklist/checklist', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/checklist/checklist/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('checklist.listing', {
#             'root': '/checklist/checklist',
#             'objects': http.request.env['checklist.checklist'].search([]),
#         })

#     @http.route('/checklist/checklist/objects/<model("checklist.checklist"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('checklist.object', {
#             'object': obj
#         })

