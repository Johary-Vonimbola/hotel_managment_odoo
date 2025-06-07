from odoo import fields, models, api

class HotelBackofficeReservationLine(models.Model):
    _name = "hotel.backoffice.reservation.line"
    _description = """
        Contains the details of the reservation, like equipement and its price
    """
    equipment_id = fields.Many2one("hotel.backoffice.equipment", required=True)
    price = fields.Float(required=True, compute="_compute_price", store=True, readonly=True)
    reservation_id = fields.Many2one("hotel.backoffice.reservation", required=True)

    _sql_constraints = [
        ("check_price", "price >= 0", "The price of the equipment should be positive")
    ]

    @api.depends("equipment_id.price")
    def _compute_price(self):
        for rec in self:
            rec.price = rec.equipment_id.price
