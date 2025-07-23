from odoo import models, api
from datetime import date

class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def _compute_amount(self, base_amount, price_unit, quantity=1.0, product=None, partner=None):
        # Fallback to default
        tax_amount = super()._compute_amount(base_amount, price_unit, quantity, product, partner)

        # Get currency from context
        currency = self.env.context.get('currency_id')
        order_date = self.env.context.get('date_order', date.today())

        if currency:
            custom_rate = self.env['tax.rate.table'].get_tax_rate(currency, order_date)
            if custom_rate:
                return base_amount * (custom_rate.tax_rate / 100.0)

        return tax_amount
