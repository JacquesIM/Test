from odoo import models, fields, api
from datetime import date

class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_tax_rate = fields.Float(
        string="Custom Tax Rate",
        compute="_compute_custom_tax_rate",
        store=True
    )

    @api.depends('invoice_date', 'currency_id')
    def _compute_custom_tax_rate(self):
        TaxRate = self.env['tax.rate.table']
        for move in self:
            rate = TaxRate.get_tax_rate(move.currency_id.id, move.invoice_date or date.today())
            move.custom_tax_rate = rate.tax_rate if rate else 0.0

    def _get_tax_context(self):
        """Helper method to build tax context with currency and date"""
        return {
            'currency_id': self.currency_id.id,
            'date_order': self.invoice_date or date.today(),
        }

    def _prepare_tax_context(self):
        """Call this when computing taxes or creating invoice lines"""
        return self._get_tax_context()
