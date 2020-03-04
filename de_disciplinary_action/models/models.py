# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Disciplinary(models.Model):
    _name = 'hr.disciplinary.case'
    _description = 'this is hr module'
    _rec_name = 'name_seq'

    title = fields.Char(string='Case Name')
    employee_name = fields.Many2one('res.partner', string='Employee Name')
    description_field = fields.Text(string='Description')
    name_seq = fields.Char(string="Order Reference", required=True, readonly=True, copy=False, index=True,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hr.disciplinary.case.sequence') or _('New')
        result = super(Disciplinary, self).create(vals)
        return result

class Addaction(models.Model):
    _name = 'hr.disciplinary.action'
    _description='this is action module'
    _rec_name = 'desciplinart_case'

    desciplinart_case = fields.Char(string='Desciplinary case')
    action_type = fields.Char(string='Action Type')
    action_created_by = fields.Many2one('res.users', string='Action Created By')
    owner = fields.Char(string='Owner')
    due_date = fields.Date(string='Due Date', default =fields.Date.today)
    status = fields.Selection([('draft', 'Draft'),
                               ('in_progress', 'In Progress'),
                               ('close', 'Close'),
                               ], default='draft', string='Status')
    description_page = fields.Text(string='Description')
# class de_disciplinary_action(models.Model):
#     _name = 'de_disciplinary_action.de_disciplinary_action'
#     _description = 'de_disciplinary_action.de_disciplinary_action'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
