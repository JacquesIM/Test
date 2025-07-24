from odoo import models, api, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty', 'price_unit', 'tax_id', 'order_id.custom_tax_rate')
    def _compute_amount(self):
        for line in self:
            # Simulated LBP product cost – make dynamic later
            product_cost_lbp = 50000.0
            product_fx = 100000.0  # Avoid 0

            # Get custom tax exchange rate from order or fallback
            tax_fx = line.order_id.custom_tax_rate or 1.0

            # Prevent division by zero for FX
            if not product_fx or product_fx == 0.0:
                product_fx = 1.0

            # Calculate USD product cost
            cost_usd = product_cost_lbp / product_fx

            # Compute LBP tax based on percentage
            tax_percent = sum(line.tax_id.mapped('amount')) or 0.0
            tax_lbp = product_cost_lbp * (tax_percent / 100.0)

            # Convert tax to USD using tax_fx
            tax_usd = tax_lbp / tax_fx if tax_fx else 0.0

            # Total USD
            total_usd = cost_usd + tax_usd

            # Assign computed values
            line.price_subtotal = cost_usd
            line.price_tax = tax_usd
            line.price_total = total_usd
