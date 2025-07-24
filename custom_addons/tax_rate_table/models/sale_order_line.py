from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

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

    @api.depends('product_uom_qty', 'price_unit', 'tax_id', 'order_id.custom_tax_rate')
    def _compute_custom_usd(self):
        for line in self:
            # Replace this logic with your actual product cost and fx rates
            product_cost_lbp = 50000.0
            product_fx = 100000.0
            tax_fx = line.order_id.custom_tax_rate or 1.0

            if not product_fx or product_fx == 0.0:
                product_fx = 1.0

            cost_usd = product_cost_lbp / product_fx

            tax_percent = sum(line.tax_id.mapped('amount')) or 0.0
            tax_lbp = product_cost_lbp * (tax_percent / 100.0)
            tax_usd = tax_lbp / tax_fx if tax_fx else 0.0

            total_usd = cost_usd + tax_usd

            line.custom_price_usd = cost_usd
            line.custom_tax_usd = tax_usd
            line.custom_total_usd = total_usd
