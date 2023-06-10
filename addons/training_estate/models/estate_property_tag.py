from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"
    name = fields.Char('Property Tag', required=True, default="")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('tag_uniq', 'unique (name)', 'A property tag must be unique!')
    ]