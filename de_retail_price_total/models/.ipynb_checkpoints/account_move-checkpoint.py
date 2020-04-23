# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class DeAccountMove(models.Model):
    _inherit='account.move'

    @api.depends('invoice_line_ids.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax =retail_price_total= 0.0
            for line in order.invoice_line_ids:
                # amount_untaxed += line.price_subtotal
                test = line.quantity * line.sh_retail_price
                retail_price_total += test
                # amount_tax += line.price_tax
            order.update({
                # 'amount_untaxed': amount_untaxed,
                'retail_price_total': retail_price_total,
                # 'amount_tax': amount_tax,
                # 'amount_total': amount_untaxed + amount_tax,
            })
            
    @api.depends('invoice_line_ids.price_total')
    def _recompute_retail_price(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax =retail_price_total= 0.0
            for line in order.invoice_line_ids:
                # amount_untaxed += line.price_subtotal
                test = line.quantity * line.sh_retail_price
                retail_price_total += test
                # amount_tax += line.price_tax
            order.update({
                # 'amount_untaxed': amount_untaxed,
                'retail_price_total': retail_price_total,
                # 'amount_tax': amount_tax,
                # 'amount_total': amount_untaxed + amount_tax,
            })
#          ,inverse='_recompute_retail_price'

    retail_price_total = fields.Monetary("Retail Price Total",readonly=True ,compute='_amount_all')
