#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odoo import fields,api,models


class MultiChannelSale(models.Model):
	_inherit = 'multi.channel.sale'
	woocommerce_interval_type = fields.Selection(selection=[('minutes', 'Minutes'),
															('hours', 'Hour'),
															('days', 'Day')],
												string="Interval Type",
												default="hours")
	woocommerce_intervals = fields.Integer(string='Intervals', default=1)
	woocommerce_feed_cron = fields.Boolean(string='Feed Evaluate')
	woocommerce_is_import = fields.Boolean(string='Import', default=False,)
	woocommerce_is_export = fields.Boolean(string='Export', default=False,)
	# woocommerce_import_product_date = fields.Date(string="Import Product Date",
	# 										  help="Products will be imported between set date and current date")
	# woocommerce_import_customer_date = fields.Date(string="Import Customer Date",
	# 										  help="Customers will be imported between set date and current date")
	# woocommerce_import_order_date = fields.Date(string="Import Order Date",
	# 										  help="Orders will be imported between set date and current date")
	# woocommerce_update_product_date = fields.Date(string="Update Product Date",
	# 										  help="products will be Updated on Odoo  between set date and current date")
	# woocommerce_update_customer_date = fields.Date(string="Update Customer Date",
	# 										  help="Customers will be Updated on Odoo between set date and current date")
	# woocommerce_update_order_date = fields.Date(string="Update Order Date",
	# 										  help="Orders will be Updated on Odoo between set date and current date")

	def write(self, vals):
		status = super(MultiChannelSale, self).write(vals)
		if self.channel == 'woocommerce':
			if ('woocommerce_is_import' in vals) or ('interval_number' in vals) or ('interval_type' in vals) or ('woocommerce_feed_cron' in vals):
				self.sudo().woocommerce_cron()
		return status

	def woocommerce_cron(self):
		self.sudo().woocommerce_cron_state_change()
		self.sudo().woocommerce_set_interval()
		self.sudo().woocommerce_feed_cron_change()

	def woocommerce_cron_state_change(self):
		import_vals = {'active': self.woocommerce_is_import}
		self.env.ref('woocommerce_odoo_connector.ir_cron_import_woocommerce_orders').write(import_vals)

	def woocommerce_set_interval(self):
		vals={'interval_type': self.woocommerce_interval_type, 'interval_number':self.woocommerce_intervals}
		self.env.ref('woocommerce_odoo_connector.ir_cron_import_woocommerce_orders').write(vals)

	def woocommerce_feed_cron_change(self):
		vals = {'active': self.woocommerce_feed_cron}
		self.env.ref('odoo_multi_channel_sale.cron_import_product').write(vals)
		self.env.ref('odoo_multi_channel_sale.cron_import_category').write(vals)
		self.env.ref('odoo_multi_channel_sale.cron_import_partner').write(vals)
		self.env.ref('odoo_multi_channel_sale.cron_import_order').write(vals)
