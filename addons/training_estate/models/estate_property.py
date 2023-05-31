from odoo import fields, models

class EstateModel(models.Model):
    _name = "estate.property"
    # sampai baris sini sudah cukup buat bikin tabel
    _description = "Estate Property models"
    name = fields.Char('Estate Name', required=True, default="Unknown")
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    description = fields.Text('Estate Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', copy=False, default=lambda self: fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Sell Price', readonly=True, copy=False)
    bedrooms = fields.Integer('BedRooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation is used to show garden orientation"
    )