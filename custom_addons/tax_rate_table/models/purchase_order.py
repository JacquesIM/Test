from odoo import models, fields, api
from datetime import date

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    custom_tax_rate = fields.Float(
        string="Custom Tax Exchange Rate",
        compute="_compute_custom_tax_rate",
        store=True,
        readonly=True
    )

    @api.depends('date_order', 'currency_id')
    def _compute_custom_tax_rate(self):
        TaxRate = self.env['tax.rate.table']
        for order in self:
            rate = TaxRate.get_tax_rate(
                currency_id=order.currency_id.id,
                rate_date=order.date_order or date.today()
            )
            order.custom_tax_rate = rate.tax_rate if rate else 1.0  # Default fallback rate

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()

        # 🧩 Propagate important context fields to invoice
        invoice_vals.update({
            'custom_tax_rate': self.custom_tax_rate,
            'currency_id': self.currency_id.id,
            'invoice_date': self.date_order,
        })

        return invoice_vals
