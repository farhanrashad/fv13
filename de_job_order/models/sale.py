# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class JobOrder(models.Model):
	_inherit = 'sale.order'
	
	job_order_ids = fields.One2many('job.order', 'sale_id', string='Job Orders')
	job_order_count = fields.Integer(string='Job Order', compute='_compute_job_order_count')
	
	@api.depends('job_order_ids')
	def _compute_job_order_count(self):
		job_order_data = self.env['job.order'].sudo().read_group([('sale_id', 'in', self.ids)], ['sale_id'], ['sale_id'])
		mapped_data = dict([(r['job_order_id'][0], r['job_order_id_count']) for r in job_order_data])
		for job in self:
			job.job_order_count = mapped_data.get(job.id, 0)
			
	def action_view_job_orders(self):
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': _('Job Orders'),
			'res_model': 'job.order',
			'view_mode': 'tree,form',
			'domain': [('sale_id', '=', self.id)],
			'context': dict(self._context, create=False, default_company_id=self.company_id.id, default_job_order_id=self.id),
		}