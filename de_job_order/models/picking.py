# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class Picking(models.Model):
	_inherit = 'stock.picking'
    
	#job_order_id = fields.Many2one('job.order', related='purchase_id.job_order_id', string='Job Order', readonly=True, store=True)
	job_order_id = fields.Many2one("job.order", related='purchase_id.job_order_id', string="Job Order", readonly=True, required=True)
	
	#@api.depends('purchase_id')
	#def _compute_Job_order_id(self):
		#self.job_order_id = self.purchase_id.job_order_id.id