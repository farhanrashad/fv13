from odoo import models, fields, api, _
from odoo import exceptions 
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    
    def salary_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'name': 'Tasks',
            'domain': [('employee_id','=', self.name)],
            'target': 'current',
            'res_model': 'hr.employee.advance.salary',
            'view_mode': 'tree,form',
        }
    
    def get_advance_salary_count(self):
        count = self.env['hr.employee.advance.salary'].search_count([('employee_id', '=', self.name)])
        self.advance_sal_req = count
    ad_check = fields.Boolean(string='Allow advance salary')    
    advance_sal_req = fields.Integer(string='Salary Request', compute='get_advance_salary_count')
    sal_limit = fields.Float(string='Advance Salary Amount', store =True, attrs={'invisible': ['|',('ad_check','=', False)]})
    sal_req_limit = fields.Integer(string='Advance Salary Limit', store=True, attrs={'invisible': ['|',('ad_check','=', False)]})
    
    
    

    
    
class EmployeeAdvanceSalary(models.Model):
    _name = 'hr.employee.advance.salary'
    _description = 'HR Employee Advance Salary'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'
    
    
    def payment_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'domain': [('communication','=', self.name)],
            'name': 'Tasks',
            'target': 'current',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
        }
    
    
 
    
    def action_send_email(self):
        
        self.ensure_one()
        self.request_date = datetime.today() 
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
        'default_template_id': template_id,

        'default_composition_mode': 'comment',
        
        'force_email': True,   

        }
        self.write({
            'state': 'request',
        }) 

        return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

        }
        
        
    
    def action_send_email_approve(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template_approve')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
          'default_template_id': template_id,

       'default_composition_mode': 'comment',

        }
        self.write({
            'state': 'approval',
        }) 

        return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

        }
        
        
    
    
    def action_send_email_reject(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template_reject')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
           'default_template_id': template_id,

          'default_composition_mode': 'comment',

        }
        self.write({
            'state': 'close',
        }) 

        return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

       }
    
    def action_send_email_confirm(self):
        self.ensure_one()
        self.confirm_date = datetime.today()
        self.conf_manager_id = self._uid
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template_confirm')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
           'default_template_id': template_id,

           'default_composition_mode': 'comment',

        }
        self.write({
            'state': 'hrconfirm',
         })  

        return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

        }
    
    
    def unlink(self):
        for leave in self:
            if leave.state in ('hrconfirm','paid'):
                raise UserError(_('You cannot delete an order form  which is not draft or close. '))
     
            return super(EmployeeAdvanceSalary, self).unlink()
        
              


    



    
    
    
    
    
    def action_case_send(self):
        template_id = self.env.ref('de_employee_disciplinary_case.email_template_edi_disciplinary_case').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.write({
            'state': 'response',
        })    
        
    def action_paid(self):
        if  not self.payment_method:
            raise exceptions.ValidationError('Please Define Payment Method and Paid amount.')
        elif self.paid_amount > self.amount:
            raise exceptions.ValidationError('Paid Amount must be less than or equal to Request Amount.')
        vals = {
            'payment_type': 'outbound',
#             'partner_type': 'customer',
            'partner_id': self.employee_id.id,
            'amount': self.paid_amount,
            'payment_date': self.confirm_date,
            'communication': self.name,
            'journal_id': self.payment_method.id,
            'payment_method_id': self.payment_method.id,

        }
        self.env['account.payment'].create(vals)
        self.write({
            'state': 'paid',
        })    
       
    def action_close_case(self):
        self.write({
            'state': 'close',
        })    
        

    name = fields.Char(string='Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True, required=True)
    request_date = fields.Date(string='Request Date', store=True, readonly=True,)
    confirm_date = fields.Date(string='Confirm Date', store=True, readonly=True,)
    amount = fields.Float(string='Request Amount', required=True)
    manager_id = fields.Many2one('hr.employee',string='Department Manager', store=True, readonly=True, related='employee_id.parent_id')
    conf_manager_id = fields.Many2one('hr.employee',string='Confirm Manager', store=True, readonly=True,)
    emp_partner_id = fields.Many2one('hr.employee', string='Employee Partner', store=True, )
    payment_method = fields.Many2one('account.journal', string='Payment Method', store=True,)
    paid_amount = fields.Float(string='Paid Amount', store=True,)

    note = fields.Html(string="Reason" ,)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('request', 'Request'),
        ('approval', 'Approval'),
        ('hrconfirm', 'HR Confirm'),        
        ('paid', 'Paid'),
        ('close','Close')
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    department_id = fields.Many2one('hr.department', string='Department', readonly=True ,related='employee_id.department_id')
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.advance.salary') or _('New')
        res = super(EmployeeAdvanceSalary,self).create(vals)
        return res
    
    

    
    
    @api.onchange('employee_id')
    def onchange_employee(self):
        test_here = self.env['hr.employee.advance.salary'].search([('employee_id.name','=', self.employee_id.name),('state','=', 'draft')])
        for rec in test_here:
            if rec.employee_id.name == self.employee_id.name:
                raise exceptions.ValidationError('You Have Already Create' +' '+ self.name + ' ' + 'Salary Request which is in draft.')
            else:
                pass
        if self.employee_id:    
            if self.employee_id.sal_limit == 0:
                raise exceptions.ValidationError('Plaese define' +' '+ str(self.employee_id.name) +' '+'Advance Salary Limit Amount.') 
        user_obj = self.env['hr.employee.advance.salary'].search([('employee_id','=', self.employee_id.id)])
        sum = 0
        for count in user_obj:
            sum = sum + 1
        if sum == self.employee_id.sal_req_limit:
            raise exceptions.ValidationError('You can create maximum'+ ' ' + str(self.employee_id.sal_req_limit) + ' ' + 'Advance Salary request Per Year.')
        else:
            pass    
        
    

        
    
    @api.onchange('amount')
    def onchange_amount(self):
        if self.employee_id.sal_limit < self.amount:
            raise exceptions.ValidationError('Advance Salary Amount Must be less than' + ' ' +str(self.employee_id.sal_limit))
        else:
            pass
        
        
   

            
            
            