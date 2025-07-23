from odoo import models, fields, api
from datetime import date

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    custom_tax_rate = fields.Float(
        string="Custom Tax Rate",
        compute="_compute_custom_tax_rate",
        store=True
    )

    @api.depends('date_order', 'currency_id')
    def _compute_custom_tax_rate(self):
        TaxRate = self.env['tax.rate.table']
        for order in self:
            rate = TaxRate.get_tax_rate(order.currency_id.id, order.date_order or date.today())
            order.custom_tax_rate = rate.tax_rate if rate else 0.0
