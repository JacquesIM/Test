from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class TaxRateTable(models.Model):
    _name = 'tax.rate.table'
    _description = 'Tax Rate Table'
    _order = 'date desc'

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    base_unit = fields.Float(string="Base Unit", default=1.0, required=True)
    tax_rate = fields.Float(string="Tax Rate", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", required=True)

    _sql_constraints = [
        ('unique_currency_date', 'unique(currency_id, date)', 'Tax rate must be unique per currency and date.')
    ]

    @api.constrains('currency_id', 'date')
    def _check_duplicate_date(self):
        for record in self:
            duplicates = self.search_count([
                ('currency_id', '=', record.currency_id.id),
                ('date', '=', record.date),
                ('id', '!=', record.id)
            ])
            if duplicates:
                raise ValidationError("A tax rate for this currency and date already exists.")

    @api.model
    def get_tax_rate(self, currency_id, on_date=None):
        """
        Returns the latest tax rate for the given currency before or on the given date.
        """
        on_date = on_date or date.today()
        return self.search([
            ('currency_id', '=', currency_id),
            ('date', '<=', on_date)
        ], order='date desc', limit=1)
