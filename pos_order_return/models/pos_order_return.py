# -*- coding: utf-8 -*-
from odoo.tools.translate import _
from odoo.tools import float_is_zero
from odoo import api, fields, models
from odoo.exceptions import UserError, Warning
import requests
import json
import datetime
import traceback


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	not_returnable = fields.Boolean('Not Returnable')


class PosOrder(models.Model):
	_inherit = 'pos.order'

	is_return_order = fields.Boolean(string='Return Order', copy=False)
	return_order_id = fields.Many2one('pos.order', 'Return Order Of', readonly=True, copy=False)
	return_status = fields.Selection([('-','Not Returned'),('Fully-Returned','Fully-Returned'),('Partially-Returned','Partially-Returned'),('Non-Returnable','Non-Returnable')],default='-',copy=False,string='Return Status')

	@api.model
	def _process_order(self, pos_order):
		prec_acc = self.env['decimal.precision'].precision_get('Account')
		pos_session = self.env['pos.session'].browse(pos_order['pos_session_id'])
		if pos_session.state == 'closing_control' or pos_session.state == 'closed':
			pos_order['pos_session_id'] = self._get_valid_session(pos_order).id
		if pos_order['is_return_order']:
			pos_order['amount_paid'] = 0
			for line in pos_order['lines']:
				line_dict = line[2]
				line_dict['qty'] = line_dict['qty']
				if line_dict.get('original_line_id'):
					original_line = self.env['pos.order.line'].browse(line_dict.get('original_line_id'))
					original_line.line_qty_returned += abs(line_dict['qty'])
			for statement in pos_order['statement_ids']:
				statement_dict = statement[2]
				if pos_order['amount_total'] <0:
					statement_dict['amount'] = statement_dict['amount'] * -1
				else:
					statement_dict['amount'] = statement_dict['amount']
			pos_order['amount_tax'] = pos_order['amount_tax']
			pos_order['amount_return'] = 0
			pos_order['amount_total'] = pos_order['amount_total']

		order = self.create(self._order_fields(pos_order))
		journal_ids = set()
		for payments in pos_order['statement_ids']:
			if not float_is_zero(payments[2]['amount'], precision_digits=prec_acc):
				order.add_payment(self._payment_fields(payments[2]))
			journal_ids.add(payments[2]['journal_id'])

		if pos_session.sequence_number <= pos_order['sequence_number']:
			pos_session.write({'sequence_number': pos_order['sequence_number'] + 1})
			pos_session.refresh()

		if not float_is_zero(pos_order['amount_return'], prec_acc):
			cash_journal_id = pos_session.cash_journal_id.id
			if not cash_journal_id:
				# Select for change one of the cash journals used in this
				# payment
				cash_journal = self.env['account.journal'].search([
					('type', '=', 'cash'),
					('id', 'in', list(journal_ids)),
				], limit=1)
				if not cash_journal:
					# If none, select for change one of the cash journals of the POS
					# This is used for example when a customer pays by credit card
					# an amount higher than total amount of the order and gets cash back
					cash_journal = [statement.journal_id for statement in pos_session.statement_ids if statement.journal_id.type == 'cash']
					if not cash_journal:
						raise UserError(_("No cash statement found for this session. Unable to record returned cash."))
				cash_journal_id = cash_journal[0].id
			order.add_payment({
				'amount': -pos_order['amount_return'],
				'payment_date': fields.Datetime.now(),
				'payment_name': _('return'),
				'journal': cash_journal_id,
			})
		return order

	@api.multi
	def action_pos_order_invoice(self):	
		Invoice = self.env['account.invoice']
		for order in self:	
			if not order.is_return_order or (order.is_return_order and order.amount_total>=0):
				super(PosOrder,order).action_pos_order_invoice()
			else:
				local_context = dict(self.env.context, force_company=order.company_id.id, company_id=order.company_id.id)
				if order.invoice_id:
					Invoice += order.invoice_id
					continue

				if not order.partner_id:
					raise UserError(_('Please provide a partner for the sale.'))
				invoice_data= {
					'name': order.name,
					'origin': order.name,
					'account_id': order.partner_id.property_account_receivable_id.id,
					'journal_id': order.session_id.config_id.invoice_journal_id.id,
					'company_id': order.company_id.id,
					'type': 'out_refund',
					'reference': order.name,
					'partner_id': order.partner_id.id,
					'comment': order.note or '',
					'currency_id': order.pricelist_id.currency_id.id,
					'user_id': order.env.uid,
				}

				invoice = Invoice.new(invoice_data)
				invoice._onchange_partner_id()
				invoice.fiscal_position_id = order.fiscal_position_id

				inv = invoice._convert_to_write({name: invoice[name] for name in invoice._cache})
				new_invoice = Invoice.with_context(local_context).sudo().create(inv)
				message = _("This invoice has been created from the point of sale session: <a href=# data-oe-model=pos.order data-oe-id=%d>%s</a>") % (order.id, order.name)
				new_invoice.message_post(body=message)
				order.write({'invoice_id': new_invoice.id, 'state': 'invoiced'})
				Invoice += new_invoice

				for line in order.lines:
					actual_qty = line.qty 
					line.qty = line.qty * -1
					self.with_context(local_context)._action_create_invoice_line(line, new_invoice.id)
					line.qty = actual_qty

				new_invoice.with_context(local_context).sudo().compute_taxes()
				order.sudo().write({'state': 'invoiced'})

			if not Invoice:
				return {}

			return {
				'name': _('Customer Invoice'),
				'view_type': 'form',
				'view_mode': 'form',
				'view_id': self.env.ref('account.invoice_form').id,
				'res_model': 'account.invoice',
				'context': "{'type':'out_refund'}",
				'type': 'ir.actions.act_window',
				'nodestroy': True,
				'target': 'current',
				'res_id': Invoice and Invoice.ids[0] or False,
			}

	def return_fbr_pos_data(self, pos_order_data):
		prev_order = self.env['pos.order'].search([('id', '=', pos_order_data.get('return_order_id'))])
		print('prev', prev_order, prev_order.pos_reference.partition(' ')[2])
		fbr_url = 'http://fbrapp.shopbrumano.com/rest/invoice/'
		header = {"Content-Type": "multipart/form-data"}
		invoice_number = ''
		if pos_order_data:
			try:
				order_dic = {
					'InvoiceNumber': '',
					'USIN': pos_order_data.get('name').partition(' ')[2],
					'RefUSIN': prev_order.pos_reference.partition(' ')[2],
					'DateTime': pos_order_data.get('creation_date'),
					'TotalBillAmount': abs(pos_order_data.get('amount_total')),
					'TotalSaleValue': abs(pos_order_data.get('amount_total') - pos_order_data.get('amount_tax')),
					'TotalTaxCharged': abs(pos_order_data.get('amount_tax')),
					'PaymentMode': 1,
					'InvoiceType': 3,
				}
				session = self.env['pos.session'].sudo().search([('id', '=', pos_order_data.get('pos_session_id'))])
				if session:
					header.update({'Authorization': session.config_id.fbr_authorization})
					order_dic.update({'POSID': session.config_id.pos_id})
				partner = False
				if pos_order_data.get('partner_id'):
					partner = self.env['res.partner'].sudo().search([('id', '=', pos_order_data.get('partner_id'))])
					order_dic.update({
						'BuyerName': partner.name,
						'BuyerPhoneNumber': partner.mobile,
					})
				if pos_order_data.get('lines'):
					items_list = []
					total_qty = 0.0
					for line in pos_order_data.get('lines'):
						product_dic = line[2]
						total_qty += product_dic.get('qty')
						if 'product_id' in product_dic:
							product = self.env['product.product'].sudo().search([
								('id', '=', product_dic.get('product_id'))])
							if product:
								fpos = False
								if pos_order_data.get('fiscal_position_id'):
									fpos = pos_order_data.get('fiscal_position_id')
									fpos = self.env['account.fiscal.position'].sudo().browse \
										(pos_order_data.get('fiscal_position_id'))
								tax_list = product_dic.get('tax_ids')[0][2]
								tax_ids = self.env['account.tax'].sudo().search([('id', 'in', tax_list)])
								pricelist_id = pos_order_data.get('pricelist_id')
								pricelist = self.env['product.pricelist'].sudo().browse(pricelist_id)
								tax_ids_after_fiscal_position = fpos.map_tax(tax_ids, product,
																			 partner) if fpos else tax_ids
								price = float(product_dic.get('price_unit')) * (
										1 - (product_dic.get('discount') or 0.0) / 100.0)
								taxes = tax_ids_after_fiscal_position.compute_all(price, pricelist.currency_id,
																				  product_dic.get('qty'),
																				  product=product, partner=partner)
								line_dic = {
									'ItemCode': product.default_code,
									'ItemName': product.name,
									'Quantity': abs(product_dic.get('qty')),
									'PCTCode': product.pct_code,
									'TaxRate': tax_ids.amount,
									'SaleValue': product_dic.get('price_unit'),
									'TotalAmount': abs(taxes['total_included']),
									'TaxCharged': abs(taxes['total_included'] - taxes['total_excluded']),
									'InvoiceType': 3,
									'RefUSIN': prev_order.pos_reference.partition(' ')[2],
								}
								items_list.append(line_dic)
					order_dic.update({'Items': items_list, 'TotalQuantity': abs(total_qty)})
				files = []
				headers = {}
				payload = {'api_key': session.config_id.fbr_authorization, 'api_data': json.dumps(order_dic)}
				payment_response = requests.request("POST", fbr_url, headers=headers, data=payload, files=files)
				print('pay1', payload)
				r_json = payment_response.json()
				pos_order = self.env['pos.order'].search([('id', '=', pos_order_data.get('return_order_id'))])
				return_order = self.env['pos.order'].search([('return_order_id', '=', pos_order.id)])
				res = r_json.get('res')
				invoice_number = res.get('invoice_no')
				# return_order.write({'return_data_fbr': True, 'return_invoice_number': invoice_number})
			except Exception as e:
				values = dict(
					exception=e,
					traceback=traceback.format_exc(),
				)

			return invoice_number

	@api.model
	def _order_fields(self,ui_order):
		print('ui_order', ui_order)
		fields_return = super(PosOrder,self)._order_fields(ui_order)
		fields_return.update({
			'is_return_order':ui_order.get('is_return_order') or False,
			'return_order_id':ui_order.get('return_order_id') or False,
			'return_status':ui_order.get('return_status') or False,
			})
		if ui_order.get('is_return_order') == True:
			print('order is returned.')
			call = self.return_fbr_pos_data(ui_order)
			print('call', call)
			fields_return.update({
				'return_data_fbr': True,
				'return_invoice_number': call
			})
		print('returned')
		return fields_return


class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'
	line_qty_returned = fields.Integer('Line Returned', default=0)
	original_line_id = fields.Many2one('pos.order.line', "Original line")

	@api.model
	def _order_line_fields(self,line,session_id=None):
		fields_return = super(PosOrderLine,self)._order_line_fields(line,session_id)
		fields_return[2].update({'line_qty_returned':line[2].get('line_qty_returned','')})
		fields_return[2].update({'original_line_id':line[2].get('original_line_id','')})
		return fields_return
