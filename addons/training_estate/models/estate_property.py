from odoo import fields, models, api

class EstateModel(models.Model):
    _name = "estate.property"
    # sampai baris sini sudah cukup buat bikin tabel
    _description = "Estate Property models"
    name = fields.Char('Estate Name', required=True, default="Unknown")
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('BedRooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation is used to show garden orientation"
    )
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Estate condition"
    )
    active = fields.Boolean(default=True)
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    property_type_id = fields.Many2one("estate.property.type", String="Estate property type")
    user_id = fields.Many2one('res.users', string='Salesman',  default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(compute='_compute_total_area', string="Total area (sqm)")
    best_price = fields.Float(compute='_compute_best_price', string="Best Price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else: record.best_price = 0.0