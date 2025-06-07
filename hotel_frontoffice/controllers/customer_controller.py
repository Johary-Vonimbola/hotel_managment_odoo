from odoo import http
from odoo.http import request
from datetime import date, timedelta

class HotelFrontoffice(http.Controller):
    @http.route('/', auth='user', website=True)
    def index(self, **kw):
        return request.render('hotel_frontoffice.homepage', {
            'rooms': request.env["hotel.backoffice.room"].search([
                ("state", "=", "available")
            ])
        })

    @http.route("/hotel/book", auth="user", website=True)
    def booking(self, room_id = None, **kw):
        try:
            room_id = int(room_id)
        except (TypeError, ValueError):
            return request.not_found()
        
        room = request.env["hotel.backoffice.room"].browse(room_id)
        equipments = request.env["hotel.backoffice.equipment"].search([
            ('id', 'not in', room.equipment_ids.ids)
        ])
        today = date.today()
        return request.render('hotel_frontoffice.room_details', {
            'room': room,
            'today': today,
            'tomorrow': today + timedelta(days=1),
            'equipments': equipments
        })
    
    def _generate_reservation_lines(self, equipments):
        return [(0, 0, {
            "equipment_id": eq.id,
            "price": eq.price
        }) for eq in equipments]

    def _manage_integer_casting(self, equipment_ids):
        result = []
        if equipment_ids is not None:
            if isinstance(equipment_ids, list):
                result = [int(eq) for eq in equipment_ids]
            else:
                result = [int(equipment_ids)]
        return result
    
    def _get_current_user(self):
        return request.env.user

    @http.route("/hotel/book/submit", methods=["POST"], website=True, auth="user", type="http")
    def submit_booking(self, **post):
        room_id = int(post.get("room_id"))
        check_in = post.get("check_in")
        check_out = post.get("check_out")
        occupants = int(post.get("nb_of_occupants"))
        equipment_ids = post.get("added_equipments")

        equipment_ids = self._manage_integer_casting(equipment_ids)

        equipments = map(lambda eq : request.env["hotel.backoffice.equipment"].browse(eq), equipment_ids)

        reservation_lines = self._generate_reservation_lines(equipments)
        
        request.env["hotel.backoffice.reservation"].sudo().create({
            "name": f"RES - {str(date.today())}",
            "room_id": room_id,
            "client_id": self._get_current_user().id,
            "check_in": check_in,
            "check_out": check_out,
            "nb_of_occupants": occupants,
            "reservation_line_ids": reservation_lines
        })

        return request.redirect("/")

    @http.route("/hotel/reservations", auth="user", website=True)
    def get_my_reservation(self, **kw):
        reservations = request.env["hotel.backoffice.reservation"].search([
            ('client_id', '=', self._get_current_user().id)
        ])
        return request.render('hotel_frontoffice.my_reservation', {
            "reservations": reservations
        })

    @http.route("/hotel/reservations/details", auth="user", website=True)
    def get_reservation_details(self, reservation_id, **kw):
        try:
            reservation_id = int(reservation_id)
        except (TypeError, ValueError):
            return request.not_found()

        reservation = request.env["hotel.backoffice.reservation"].sudo().browse(reservation_id)
        if not reservation or reservation.client_id.id != self._get_current_user().id:
            return request.not_found()

        return request.render("hotel_frontoffice.my_reservation_details", {
            "reservation": reservation,
            "lines": reservation.reservation_line_ids
        })

    @http.route("/hotel/reservations/update_state", website=True, auth="user")    
    def check_in_reservation(self, state = None, reservation_id = None, **kw):
        try:
            reservation_id = int(reservation_id)
        except (TypeError, ValueError):
            return request.not_found()
        reservation = request.env["hotel.backoffice.reservation"].sudo().browse(reservation_id)
        if not reservation:
            return request.not_found()

        if state is not None:
            if state == 'check_in':
                reservation.state_check_in()
            elif state == 'check_out':
                reservation.state_check_out()
            else:
                reservation.state_cancel()
        else:
            request.not_found()
        return request.redirect(f"/hotel/reservations/details?reservation_id={reservation_id}")


    # @http.route('/hotel_frontoffice/hotel_frontoffice/objects', auth='user')
    # def list(self, **kw):
    #     return http.request.render('hotel_frontoffice.listing', {
    #         'root': '/hotel_frontoffice/hotel_frontoffice',
    #         'objects': http.request.env['hotel_frontoffice.hotel_frontoffice'].search([]),
    #     })

    # @http.route('/hotel_frontoffice/hotel_frontoffice/objects/<model("hotel_frontoffice.hotel_frontoffice"):obj>', auth='user')
    # def object(self, obj, **kw):
    #     return http.request.render('hotel_frontoffice.object', {
    #         'object': obj
    #     })

