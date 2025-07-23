from odoo import models, api

class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None, is_refund=False):
        res = super().compute_all(price_unit, currency, quantity, product, partner, is_refund)

        currency_id = self.env.context.get('currency_id')
        date_order = self.env.context.get('date_order')

        if currency_id and date_order:
            custom_rate = self.env['tax.rate.table'].get_tax_rate(currency_id, date_order)
            if custom_rate:
                for tax in res['taxes']:
                    tax['amount'] = price_unit * quantity * (custom_rate.tax_rate / 100.0)
                    tax['tax_rate'] = custom_rate.tax_rate  # optional for tracking

                # Recalculate totals using the custom tax amounts
                res['total_excluded'] = price_unit * quantity
                res['total_included'] = res['total_excluded'] + sum(t['amount'] for t in res['taxes'])

        return res
