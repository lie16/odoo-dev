from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


# from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float('Price', required=True, default="0.00")
    status = fields.Selection(
        string='Status',
        selection=[('y', 'Accepted'), ('n', 'Refused')],
        help="Offering status"
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    validity = fields.Integer('Validity (days)', required=True, default=7, stored=True)
    date_deadline = fields.Date('Deadline', compute='_compute_validity', inverse='_inverse_validity', required=True,
                                stored=True)

    _sql_constraints = [
        ('cek_offer_price', 'CHECK(price >= 0)',
         'The price should be postive.')
    ]

    @api.depends('validity')
    def _compute_validity(self):
        for record in self:
            if record.create_date:
                start_date = record.create_date
            else:
                start_date = fields.Datetime.now().date()
            if record.validity:
                duration = record.validity
            else:
                duration = 0
            # record.date_deadline = start_date + timedelta(days=duration)
            record.date_deadline = fields.Datetime.add(start_date, days=duration)

    def _inverse_validity(self):
        for record in self:
            if record.create_date:
                createdate = record.create_date
            else:
                createdate = fields.Datetime.now()
            # print('Tanggal date: %s' % createdate)
            duration = record.date_deadline - createdate.date()
            # print('Duration: %s' % duration.days)
            record.validity = duration.days
            # record.validity fields.datetime.
            # print('Validity: %s' % record.validity)

    def accept(self):
        for record in self:
            record.status = "y"
            record.property_id.state = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
        return True

    def reject(self):
        for record in self:
            record.status = "n"
        return True

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Offering price must be postive")

    @api.constrains('status', 'property_id.expected_price')
    def _check_status(self):
        for record in self:
            # print("record.status = %s" % record.status)
            if record.status == "y":
                # print("record.property_id.expected_price = %s" % record.property_id.expected_price)
                # print("record.property_id.selling_price = %s" % record.property_id.selling_price)
                if float_is_zero(record.property_id.selling_price, precision_rounding=2):
                    if float_compare(record.property_id.selling_price, (record.property_id.expected_price * 0.9),
                                     precision_rounding=2) == -1:
                        # if float_compare(record.price, (record.property_id.expected_price * 0.9), precision_rounding=2) == -1:
                        raise ValidationError("Offering price cannot be less than 90 % of selling price")
