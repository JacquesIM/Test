from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    custom_price_usd = fields.Float(
        string="Custom Cost (USD)",
        compute='_compute_custom_usd',
        store=True
    )
    custom_tax_usd = fields.Float(
        string="Custom Tax (USD)",
        compute='_compute_custom_usd',
        store=True
    )
    custom_total_usd = fields.Float(
        string="Custom Total (USD)",
        compute='_compute_custom_usd',
        store=True
    )

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'order_id.custom_tax_rate')
    def _compute_custom_usd(self):
        for line in self:
            # 👇 Placeholder: Replace with real LBP cost if available
            product_cost_lbp = 50000.0  

            # 👇 Exchange rate for converting product cost from LBP to USD
            product_fx = 100000.0

            # 👇 Custom tax exchange rate set on the Purchase Order
            tax_fx = line.order_id.custom_tax_rate or 1.0

            # Fallback if product FX is missing
            if not product_fx:
                product_fx = 1.0

            # 👇 Compute cost in USD
            cost_usd = product_cost_lbp / product_fx

            # 👇 Compute tax percent from the tax list
            tax_percent = sum(line.taxes_id.mapped('amount')) or 0.0
            tax_lbp = product_cost_lbp * (tax_percent / 100.0)

            # 👇 Compute tax in USD using tax exchange rate
            tax_usd = tax_lbp / tax_fx if tax_fx else 0.0

            # 👇 Total USD = product USD + tax USD
            total_usd = cost_usd + tax_usd

            # ✅ Set values
            line.custom_price_usd = round(cost_usd, 2)
            line.custom_tax_usd = round(tax_usd, 2)
            line.custom_total_usd = round(total_usd, 2)
