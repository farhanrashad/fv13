# -*- coding: utf-8 -*-
from custom_addons import de_training_batch
from odoo import api, fields, models, _
from odoo.exceptions import UserError


# class StudentPartner(models.Model):
#     _inherit = 'res.partner'
#
#     is_student = fields.Boolean(default=False)
#
#     first_name = fields.Char(required=True)
#     middle_name = fields.Char(default=" ")
#     last_name = fields.Char(required=True)
#
#     @api.onchange('last_name')
#     def get_name(self):
#         if self.last_name:
#             self.name = self.first_name + " " + self.middle_name + " " + self.last_name