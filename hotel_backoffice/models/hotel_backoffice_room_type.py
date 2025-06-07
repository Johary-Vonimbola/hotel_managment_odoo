from odoo import fields, models

class HotelBackofficeRoomType(models.Model):
    _name = "hotel.backoffice.room.type"
    _description = """
        Model for the different types of Room : 
            -Deluxe
            -Standard
            -Executive
    """
    name = fields.Char(required=True)
    room_ids = fields.One2many("hotel.backoffice.room", "room_type_id")