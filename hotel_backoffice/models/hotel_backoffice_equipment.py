from odoo import fields, models

class HotelBackofficeEquipment(models.Model):
    _name = "hotel.backoffice.equipment"
    _description = """"
        Room's equipment that the user could add while booking a room
    """
    name = fields.Char(required=True)
    description = fields.Text()
    price = fields.Float(default = 0)
    room_ids = fields.Many2many("hotel.backoffice.room")

    _sql_constraints = [
        ("check_price", "price >= 0", "The price of the equipment should be positive")
    ]