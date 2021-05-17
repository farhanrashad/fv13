# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, modules,fields, _

class ProjectTaskExt(models.Model):
    _inherit = 'project.task'

    @api.onchange('color')
    def onchange_color(self):
        self.color_icon = self.color

    color = fields.Selection(string="Color", selection=[
        ('black', "None"),
        ('grey', "Grey"),
        ('red', "Red"),
        ('green', "Green"),
        ('purple', "Purple"),
        ('blue', "Blue"),
        ('brown', "Brown")], default="black", required=True)

    color_icon = fields.Selection([
        ('black', "None"),
        ('grey', "Grey"),
        ('red', "Red"),
        ('green', "Green"),
        ('purple', "Purple"),
        ('blue', "Blue"),
        ('brown', "Brown")], string='~')
