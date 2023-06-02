from odoo import fields, models


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

