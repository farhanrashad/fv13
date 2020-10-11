from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning

   
class JobPositionRequest(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='hr.job.position.request'
    _description="Job Position Request"
    
    def job_position_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
#             'domain':[('project_id','=',self.name)],
            'name': 'Tasks',
            'target': 'current',
            'res_model': 'hr.job',
            'view_mode': 'tree,form',
        }
    

 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('verify', 'HOD Approval'),
        ('co_approve', 'HR Manager'),
        ('done', 'Done'),
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    
    def _get_default_stage_id(self):
        return self.env['job.position.stages'].search([], limit=1).id
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['job.position.stages'].search([])
        return stage_ids

    stage_id = fields.Many2one('job.position.stages', string='Stage', ondelete='restrict', tracking=True, index=True,
        group_expand='_read_group_stage_ids',
         default=_get_default_stage_id,
         copy=False)
    
    
    def unlink(self):
        for leave in self:
            if leave.state in ('done','verify','co_approve'):
                raise UserError(_('You cannot delete an order form  which is not draft or cancelled. '))
     
            return super(JobPositionRequest, self).unlink()
    
   

        
    def draft(self):
        self.write({'state':'submit'}) 
        
    def submit(self):
        self.write({'state':'verify'}) 
        
    def verify(self):
        self.write({'state':'co_approve'})    
        
    def co_approve(self):
        self.env['hr.job'].create({'name': self.name,
                                            'department_id':self.department.id,
                                            'no_of_recruitment':self.no_of_person_request,
                                            'user_id':self.requested_by.id,
                                            })
        self.write({'state':'done'})    
   
   

    
    date=fields.Date("Request On" ,default=datetime.today())
    no_of_person_request=fields.Integer('Expected new employee',default="1")
#     gender_preference=fields.Selection([
#         ('male', 'Male'),
#         ('female', 'Female'),
#         ('trans', 'Transgender'),
#         ], string='Gender Preferences')
    budget=fields.Boolean('Budgeted')
    department=fields.Many2one('hr.department',"Department",required=True)
#     team=fields.Many2one('hr.team','Team')
        
    requested_by=fields.Many2one('res.users','Requested By',  default=lambda self: self.env.user,readonly=True)
#     reported_to=fields.Many2one('res.users','Reporting To')

    reason = fields.Text('Reason')
#     job_position=fields.Many2one('hr.job','Job Position')
    age_preference=fields.Integer('Age Preference',default="0")
    get_id=fields.Char('Order', readonly=True, copy=False,)
    name= fields.Char('Name', required=True)
    qualification= fields.Html('Qualifications / Background / Skills Set')
    education= fields.Html('Education / Degree Required')
    software= fields.Html('Software Proficiency Requirements')
    communication= fields.Html('Communications')
    preferences_ids=fields.One2many('hr.preferences', 'position_id', string='')

    
    
    @api.model
    def create(self, vals):
        if 'get_id' not in vals or vals['get_id'] == False:
            sequence = self.env.ref('open_hcm_job_position_request.get_id')
            vals['get_id'] = sequence.next_by_id()
        return super(JobPositionRequest, self).create(vals)
    
    
class HrTeam(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='hr.team'
    _description="Team Form"


    name=fields.Char('Name',required=True)
    
class Preferences(models.Model):
    _name='hr.preferences'
    _description="Preferences Form"


    pref_name=fields.Char('Name',required=True)
    pref_value=fields.Char('Value',required=True)
    position_id=fields.Many2one('hr.job.position.request', string='')


        
class JobpositionStages(models.Model):
    _name = 'job.position.stages'
    _description = 'Position Stage'
    
    

    def _get_default_project_ids(self):
        default_project_id = self.env.context.get('default_project_id')
        return [default_project_id] if default_project_id else None

    name = fields.Char(string='Stage Name', required=True, translate=True)
#     user_id = fields.Many2one('res.users',string='User', store=True)
    is_quality = fields.Boolean(string='Active')
        