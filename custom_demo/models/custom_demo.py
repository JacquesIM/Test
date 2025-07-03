from odoo import models, fields

class CustomDemo(models.Model):
    _name = "custom.demo"
    _description = "Custom Demo"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
