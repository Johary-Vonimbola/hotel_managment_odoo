from odoo import fields, models, api

class HotelBackofficeRoom(models.Model):
    _name = "hotel.backoffice.room"
    _description = """
        Model for Rooms
    """
    name = fields.Char(required=True)
    max_allowed_person = fields.Integer(default=1)
    state = fields.Selection([
        ("available", "Available"),
        ("booked", "Booked"),
    ], default = "available", required=True)
    description = fields.Text()
    base_price = fields.Float()
    equipment_ids = fields.Many2many("hotel.backoffice.equipment")
    total_price = fields.Float(compute="_compute_total_price")
    room_type_id = fields.Many2one("hotel.backoffice.room.type", required=True)
    reservation_ids = fields.One2many("hotel.backoffice.reservation", "room_id")

    _sql_constraints = [
        ("check_base_price", "base_price >= 0", "The base price of the room should be positive"),
        ("check_max_allowed_person", "max_allowed_person > 0", "The max allowed person should be positive")
    ]

    @api.depends("base_price", "equipment_ids.price")
    def _compute_total_price(self):
        for rec in self:
            total_equipment_prices = sum(rec.equipment_ids.mapped("price"))
            rec.total_price = rec.base_price + total_equipment_prices
