from odoo import models, fields, api
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_tax_rate = fields.Float(
        string="Custom Tax Rate",
        compute="_compute_custom_tax_rate",
        store=True
    )

    @api.depends('date_order', 'currency_id')
    def _compute_custom_tax_rate(self):
        TaxRate = self.env['tax.rate.table']
        for order in self:
            rate = TaxRate.search([
                ('currency_id', '=', order.currency_id.id),
                ('date', '<=', order.date_order or date.today())
            ], order='date desc', limit=1)
            order.custom_tax_rate = rate.tax_rate if rate else 0.0

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['custom_tax_rate'] = self.custom_tax_rate
        invoice_vals['currency_id'] = self.currency_id.id
        invoice_vals['invoice_date'] = self.date_order
        return invoice_vals
