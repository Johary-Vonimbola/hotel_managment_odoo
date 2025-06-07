# -*- coding: utf-8 -*-
# from odoo import http


# class HotelFrontoffice(http.Controller):
#     @http.route('/hotel_frontoffice/hotel_frontoffice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_frontoffice/hotel_frontoffice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_frontoffice.listing', {
#             'root': '/hotel_frontoffice/hotel_frontoffice',
#             'objects': http.request.env['hotel_frontoffice.hotel_frontoffice'].search([]),
#         })

#     @http.route('/hotel_frontoffice/hotel_frontoffice/objects/<model("hotel_frontoffice.hotel_frontoffice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_frontoffice.object', {
#             'object': obj
#         })

