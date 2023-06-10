from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"
    name = fields.Char('Property Type', required=True, default="")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Property Type")
    active = fields.Boolean(default=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('type_uniq', 'unique (name)', 'A property type must be unique!')
    ]
