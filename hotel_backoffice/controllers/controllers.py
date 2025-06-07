# -*- coding: utf-8 -*-
# from odoo import http


# class HotelBackoffice(http.Controller):
#     @http.route('/hotel_backoffice/hotel_backoffice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_backoffice/hotel_backoffice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_backoffice.listing', {
#             'root': '/hotel_backoffice/hotel_backoffice',
#             'objects': http.request.env['hotel_backoffice.hotel_backoffice'].search([]),
#         })

#     @http.route('/hotel_backoffice/hotel_backoffice/objects/<model("hotel_backoffice.hotel_backoffice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_backoffice.object', {
#             'object': obj
#         })

