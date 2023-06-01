from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type models"
    name = fields.Char('Property Type', required=True, default="")
    active = fields.Boolean(default=True)