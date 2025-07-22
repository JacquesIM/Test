from odoo import models, fields, api
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

    @api.model
    def get_tax_rate(self, currency_id, on_date=None):
        on_date = on_date or date.today()
        return self.search([
            ('currency_id', '=', currency_id),
            ('date', '<=', on_date)
        ], order='date desc', limit=1)
