from odoo import models, api, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'order_id.custom_tax_rate')
    def _compute_amount(self):
        for line in self:
            # ⚠️ Later: Make this dynamic based on actual product
            product_cost_lbp = 50000.0
            product_fx = 100000.0

            # Fallbacks to avoid division by zero
            if not product_fx or product_fx == 0.0:
                product_fx = 1.0
            tax_fx = line.order_id.custom_tax_rate or 1.0

            # Compute USD product cost
            cost_usd = product_cost_lbp / product_fx

            # Compute LBP tax (based on tax %)
            tax_percent = sum(line.taxes_id.mapped('amount')) or 0.0
            tax_lbp = product_cost_lbp * (tax_percent / 100.0)

            # Compute USD tax
            tax_usd = tax_lbp / tax_fx if tax_fx else 0.0

            # Final totals
            total_usd = cost_usd + tax_usd

            # Assign
            line.price_subtotal = cost_usd
            line.price_tax = tax_usd
            line.price_total = total_usd
