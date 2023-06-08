from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    name = fields.Char('Property Type', required=True, default="")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Property Type")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('type_uniq', 'unique (name)', 'A property type must be unique!')
    ]
