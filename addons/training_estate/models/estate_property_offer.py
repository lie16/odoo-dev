from odoo import fields, models, api
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
    date_deadline = fields.Date('Deadline', compute='_compute_validity', inverse='_inverse_validity', required=True, stored=True)
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
            duration =  record.date_deadline - createdate.date()
            # print('Duration: %s' % duration.days)
            record.validity = duration.days
            # record.validity fields.datetime.
            # print('Validity: %s' % record.validity)

    def accept(self):
        for record in self:
            record.status="y"
            record.property_id.selling_price=record.price
            record.property_id.partner_id=record.partner_id
        return True
    def reject(self):
        for record in self:
            record.status="n"
        return True