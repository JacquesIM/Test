from odoo import models, fields, api
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_tax_rate = fields.Float(string="Custom Tax Rate", compute="_compute_custom_tax_rate", store=True)

    @api.depends('date_order', 'currency_id')
    def _compute_custom_tax_rate(self):
        for order in self:
            rate = self.env['tax.rate.table'].search([
                ('currency_id', '=', order.currency_id.id),
                ('date', '<=', order.date_order or date.today())
            ], order='date desc', limit=1)
            order.custom_tax_rate = rate.tax_rate if rate else 0.0
