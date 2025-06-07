from odoo import http
from odoo.http import request
from datetime import date, timedelta
import base64
import json

class HotelFrontofficeApi(http.Controller):

    def make_json_structure(self, code=200, data=None, status="Success", message=""):
        return {
            "code": code,
            "data": data if data is not None else [],
            "status": status,
            "message": message
        }

    def _get_current_user(self):
        return request.env.user

    def _manage_integer_casting(self, equipment_ids):
        result = []
        if equipment_ids is not None:
            if isinstance(equipment_ids, list):
                result = [int(eq) for eq in equipment_ids]
            else:
                result = [int(equipment_ids)]
        return result

    def _generate_reservation_lines(self, equipments):
        return [(0, 0, {
            "equipment_id": eq.id,
            "price": eq.price
        }) for eq in equipments]

    @http.route('/api/rooms/available', auth='public', type='http', methods=['GET'])
    def api_get_available_rooms(self, **kw):
        rooms = request.env["hotel.backoffice.room"].sudo().search([("state", "=", "available")])
        result = []
        for room in rooms:
            result.append({
                "id": room.id,
                "name": room.name,
                "price": room.total_price
            })
        data = self.make_json_structure(data=result)
        return request.make_json_response(data)

    @http.route('/api/rooms/<int:room_id>/details', auth='public', type='http', methods=['GET'])
    def api_get_room_details(self, room_id, **kw):
        room = request.env["hotel.backoffice.room"].sudo().browse(room_id)
        if not room.exists():
            return request.make_json_response(self.make_json_structure(code=404, status="Error", message="Room not found"))

        available_equipments = request.env["hotel.backoffice.equipment"].sudo().search([
            ('id', 'not in', room.equipment_ids.ids)
        ])
        data = {
            "room": {
                "id": room.id,
                "name": room.name,
                "price": room.total_price
            },
            "equipments": [{"id": eq.id, "name": eq.name, "price": eq.price} for eq in available_equipments],
            "today": str(date.today()),
            "tomorrow": str(date.today() + timedelta(days=1))
        }
        return request.make_json_response(self.make_json_structure(data=data))

    @http.route('/api/reservations', auth='public', type='http', methods=['POST'], csrf=False)
    def api_submit_booking(self, **post):
        try:
            data = json.loads(request.httprequest.data)
            room_id = int(data.get("room_id"))
            check_in = data.get("check_in")
            check_out = data.get("check_out")
            occupants = int(data.get("nb_of_occupants"))
            id = int(data.get("client_id"))
            equipment_ids = data.get("added_equipments")
            equipment_ids = self._manage_integer_casting(equipment_ids)
            equipments = [request.env["hotel.backoffice.equipment"].browse(eq_id) for eq_id in equipment_ids]
            reservation_lines = self._generate_reservation_lines(equipments)

            reservation = request.env["hotel.backoffice.reservation"].sudo().create({
                "name": f"RES - {str(date.today())}",
                "room_id": room_id,
                "client_id": id,
                "check_in": check_in,
                "check_out": check_out,
                "nb_of_occupants": occupants,
                "reservation_line_ids": reservation_lines
            })

            return request.make_json_response(
                self.make_json_structure(
                    data={"reservation_id": reservation.id},
                    message="Reservation created successfully"
                )
            )

        except Exception as e:
            return request.make_json_response(
                self.make_json_structure(code=500, status="Error", message=str(e))
            )

    @http.route('/api/reservations', auth='public', type='http', methods=['GET'])
    def api_get_my_reservations(self, **kw):
        data = json.loads(request.httprequest.data)
        user_id = data.get("client_id")
        reservations = request.env["hotel.backoffice.reservation"].sudo().search([('client_id', '=', user_id)])
        data = []
        for res in reservations:
            data.append({
                "id": res.id,
                "name": res.name,
                "room_id": res.room_id.id,
                "room_name": res.room_id.name,
                "check_in": str(res.check_in),
                "check_out": str(res.check_out),
                "nb_of_occupants": res.nb_of_occupants,
                "state": res.state
            })
        return request.make_json_response(self.make_json_structure(data=data))

    @http.route('/api/reservations/<int:reservation_id>', auth='public', type='http', methods=['GET'])
    def api_get_reservation_details(self, reservation_id, **kw):
        data = json.loads(request.httprequest.data)
        id = int(data.get("client_id"))
        reservation = request.env["hotel.backoffice.reservation"].sudo().browse(reservation_id)
        if not reservation or reservation.client_id.id != id:
            return request.make_json_response(
                self.make_json_structure(code=404, status="Error", message="Reservation not found")
            )

        data = {
            "id": reservation.id,
            "room": reservation.room_id.name,
            "check_in": str(reservation.check_in),
            "check_out": str(reservation.check_out),
            "nb_of_occupants": reservation.nb_of_occupants,
            "state": reservation.state,
            "lines": [{
                "equipment_id": line.equipment_id.id,
                "equipment_name": line.equipment_id.name,
                "price": line.price
            } for line in reservation.reservation_line_ids]
        }
        return request.make_json_response(self.make_json_structure(data=data))

    @http.route('/api/reservations/<int:reservation_id>/state', auth='public', type='http', methods=['POST'], csrf=False)
    def api_update_reservation_state(self, reservation_id, **post):
        data = json.loads(request.httprequest.data)
        state = data.get("state")
        reservation = request.env["hotel.backoffice.reservation"].sudo().browse(reservation_id)
        if not reservation:
            return request.make_json_response(
                self.make_json_structure(code=404, status="Error", message="Reservation not found")
            )

        if state == 'check_in':
            reservation.state_check_in()
        elif state == 'check_out':
            reservation.state_check_out()
        elif state == 'cancel':
            reservation.state_cancel()
        else:
            return request.make_json_response(
                self.make_json_structure(code=400, status="Error", message="Invalid state provided")
            )

        return request.make_json_response(
            self.make_json_structure(message=f"Reservation {state} successful")
        )
