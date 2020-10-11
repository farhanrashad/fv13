#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Request Job Positions',
    'category': 'Human Resources',
    'version': '13.0.1.0.0',
    'author': 'dynexcel',
    'summary': 'Daily life work',
    'description': "",
    'depends': [
        'hr',
        'hr_recruitment',
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/job_request.xml',
        'views/hr_applicant.xml',
        'views/hr_job_view.xml',
    ],
    
}
