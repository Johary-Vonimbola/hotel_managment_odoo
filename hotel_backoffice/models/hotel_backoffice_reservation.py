from odoo import fields, models, api
from datetime import timedelta, date
from odoo.exceptions import ValidationError

class HotelBackofficeReservation(models.Model):
    _name = "hotel.backoffice.reservation"
    _description = """
        Reservation model
    """
    name = fields.Char(required = True)
    check_in = fields.Date(default = date.today(), required = True, string = "Date debut")
    check_out = fields.Date(default = lambda arg : fields.Date.today() + timedelta(days=1), required = True, string = "Date fin")
    state = fields.Selection([
        ("booked", "Booked"),
        ("cancelled", "Cancelled"),
        ("check_in", "Check In"),
        ("check_out", "Check Out")
    ], default = "booked", required = True)
    nb_of_occupants = fields.Integer(required = True)
    room_id = fields.Many2one("hotel.backoffice.room", required = True)
    client_id = fields.Many2one("res.partner", required = True)
    reservation_line_ids = fields.One2many("hotel.backoffice.reservation.line", "reservation_id")
    total_reservation = fields.Float(compute = "_compute_total_reservation", store=True)
    default_equipment_ids = fields.Many2many("hotel.backoffice.equipment", related="room_id.equipment_ids")

    _sql_constraints = [
        ("check_booking_duration", "check_in < check_out", "The check in and check out could not be on the same date and check in must be inferior to check out date")
    ]

    @api.depends("state")
    def _compute_room_state(self):
        for rec in self:
            rec.room_id.state = "available" if rec.state == "check_out" or rec.state == "cancelled" else "booked"

    @api.depends("check_in")
    def _compute_check_out(self):
        for rec in self:
            rec.check_out = rec.check_in + timedelta(days=1)

    @api.depends("room_id.total_price", "reservation_line_ids.price")
    def _compute_total_reservation(self):
        for rec in self:
            total_reservation_line_prices = sum(rec.reservation_line_ids.mapped("price"))
            rec.total_reservation = total_reservation_line_prices + rec.room_id.total_price

    @api.constrains("nb_of_occupants")
    def check_nb_of_occupants(self):
        for rec in self:
            if rec.nb_of_occupants > rec.room_id.max_allowed_person:
                raise ValidationError(f"The max allowed person for this room is {rec.room_id.max_allowed_person}")
            
    def state_check_in(self):
        for rec in self:
            rec.state = "check_in"
            rec._compute_room_state()

    def state_cancel(self):
        for rec in self:
            rec.state = "cancelled"
            rec._compute_room_state()

    def state_check_out(self):
        for rec in self:
            rec.state = "check_out"
            rec._compute_room_state()


    @api.model_create_multi
    def create(self, vals):
        reservation = super(HotelBackofficeReservation, self).create(vals)
        reservation._compute_room_state()
        return reservation