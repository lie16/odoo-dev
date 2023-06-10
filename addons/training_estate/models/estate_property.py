from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare, float_is_zero


class EstateModel(models.Model):
    _name = "estate.property"
    # sampai baris sini sudah cukup buat bikin tabel
    _description = "Estate Property models"
    _order = "id desc"
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
    estate_state = fields.Char('Status')

    _sql_constraints = [
        ('cek_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price should be positive.'),
        ('cek_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be positive.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    # Onchange tidak merubah nilai di database, hanya terkait dengan reactivity di form. dan hanya bisa dengan local field
    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def change_estate_state_sold(self):
        print('self = %s' % self)
        # Loop through each record in the recordset
        for record in self:
            # Check if the estate state is 'Cancelled'
            if record.estate_state == 'Cancelled':
                # Raise an error message if it is
                raise UserError('Property had been cancelled')
            else:
                # Change the estate state to 'Sold'
                record.estate_state='Sold'
                return True

    def change_estate_state_canceled(self):
        print('self = %s' % self)
        # Loop through each record in the recordset
        for record in self:
            # Check if the estate state is 'Cancelled'
            if record.state == 'Sold':
                # Raise an error message if it is
                raise UserError('Property had been sold.')
            else:
                # Change the estate state to 'Sold'
                record.state='Cancelled'
                return True

    @api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for record in self:
            if record.expected_price < 0 or record.selling_price < 0:
                raise ValidationError("Price must be positive")
            # not sure with actual usage for these
            if record.selling_price > 0:
                if not float_is_zero(record.selling_price, precision_rounding=2):
                    if float_compare(record.selling_price, (record.expected_price * 0.9), precision_rounding=2) == -1:
                        raise ValidationError("Offering price cannot be less than 90 % of selling price")