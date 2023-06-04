from odoo import fields, models, api
from datetime import datetime, timedelta

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
    validity = fields.Integer('Validity (days)', required=True, default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_validity', required=True)
    # inverse = '_inverse_validity',
    @api.depends('validity')
    def _compute_validity(self):
        for record in self:
            print("validity = %s" % record.validity)
            if record.create_date:
                start_date = record.create_date
            else:
                start_date = fields.Datetime.now()
            if record.validity:
                duration = timedelta(days=record.validity)
            else:
                duration = 0
            record.date_deadline = start_date + duration

    # def _inverse_validity(self):
    #     for record in self:
    #         if record.create_date:
    #             createdate = fields.Datetime.now()
    #         else:
    #             createdate = record.create_date
    #         print('Tanggal date: %s' % createdate)
    #         record.validity = record.date_deadline - createdate
    #         print('Validity: %s' % record.validity)