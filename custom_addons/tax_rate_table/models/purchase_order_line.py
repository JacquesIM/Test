from odoo import models, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'order_id.custom_tax_rate')
    def _compute_amount(self):
        for line in self:
            product_cost_lbp = 50000  # Example fixed value
            product_fx = 100000
            tax_fx = line.order_id.custom_tax_rate

            cost_usd = product_cost_lbp / product_fx
            tax_lbp = product_cost_lbp * (line.taxes_id.amount / 100.0)
            tax_usd = tax_lbp / tax_fx

            total_usd = cost_usd + tax_usd

            line.price_subtotal = cost_usd
            line.price_tax = tax_usd
            line.price_total = total_usd
