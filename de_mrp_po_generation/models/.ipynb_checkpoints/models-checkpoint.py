from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class MoBeforhandWizard(models.TransientModel):
    _name = 'mrp.mo.beforehand.wizard'
    _description = 'Create PO from MO'

    mrp_id = fields.Many2one('mrp.production',string="Manufacturing Order")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
