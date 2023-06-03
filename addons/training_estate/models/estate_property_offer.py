from odoo import fields, models, api

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
    validity = fields.Integer('Validity (days)', compute='_compute_validity', required=True, default="7")
    date_deadline = fields.Date('Deadline', required=True)
    # inverse = '_inverse_validity',
    @api.depends('validity')
    def _compute_validity(self):
        for record in self:
            if record.create_date:
                date = fields.Datetime.now().date()
            else:
                date = record.create_date
            record.date_deadline = fields.Datetime.add(date, days=record.validity)

    # def _inverse_validity(self):
    #     for lead in self:
    #         if lead.partner_id and lead.email_from != lead.partner_id.email:
    #             lead.partner_id.email = lead.email_from
