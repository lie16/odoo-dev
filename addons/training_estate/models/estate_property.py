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
        help="Estate condition",
        default='new'
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
    # estate_state = fields.Char('Status')

    _sql_constraints = [
        ('cek_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price should be positive.'),
        ('cek_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be positive.'),
    ]

    @api.model
    def create(self, values):
        if 'offer_ids' in values:
            # Trigger the onchange method when offer_ids is updated
            self._onchange_offer_ids_status()
        # count = self.env['estate.property.offer'].search_count([('status', '!=', False), ('estate.property.offer.property_id', '=', self.id)])
        # print('count created: %s' % count)
        record = super(EstateModel, self).create(values)
        print('value created: %s' % values)
        # Perform your data updates here
        return record

    def write(self, values):
        if 'offer_ids' in values:
            # Trigger the onchange method when offer_ids is updated
            self._onchange_offer_ids_status()
        # count = self.env['estate.property.offer'].search_count([('status', '!=', False), ('estate.property.offer.property_id', '=', self.id)])
        # print('count write: %s' % count)
        res = super(EstateModel, self).write(values)
        print('value write: %s' % values)
        # print('self write: %s' % max(self.offer_ids))
        # Perform your data updates here
        return res

    @api.onchange('offer_ids.status')
    def _onchange_offer_ids_status(self):
        print('_onchange_offer_ids_status')
        total_offers = self._compute_total_offers()
        print('total_offers: %s' % total_offers)
        for record in self:
            if record.state == 'new' and total_offers.get(record.id, 0) > 1:
                record.state = 'received'
            # else:
            #     record.state = 'new'

    @api.model
    def _compute_total_offers(self):
        # eplanation for these part
        # self.env['estate.property.offer']: This accesses the model estate.property.offer using the Odoo environment (self.env). It creates a recordset that represents the estate.property.offer model.
        #
        # .read_group(): This method performs a grouped read operation on the model estate.property.offer. It allows us to aggregate data based on specific criteria.
        #
        # ([('property_id', 'in', self.ids), ('status', '=', False)], ['property_id'], ['property_id']): This specifies the parameters for the grouped read operation.
        #
        # ('property_id', 'in', self.ids) is a domain filter that limits the records to those where the property_id is present in the current estate.property record IDs (self.ids).
        # ('status', '=', False) further filters the records to only include those with a null status.
        # ['property_id'] indicates the field(s) to group the data by. In this case, it groups the data by the property_id field of estate.property.offer.
        # ['property_id'] specifies the field(s) to retrieve from the grouped data. Here, it retrieves the property_id field.
        offer_data = self.env['estate.property.offer'].read_group(
            [('property_id', 'in', self.ids), ('status', '=', False)],
            ['property_id'], ['property_id']
        )
        print('offer_data: %s' % offer_data)
        total_offers = {data['property_id'][0]: data['property_id_count'] for data in offer_data}
        print('total_offers: %s' % total_offers)
        return total_offers



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
            if record.state == 'Cancelled':
                # Raise an error message if it is
                raise UserError('Property had been cancelled')
            else:
                # Change the estate state to 'Sold'
                record.state='Sold'
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