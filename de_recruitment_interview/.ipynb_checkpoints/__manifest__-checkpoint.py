# -*- coding: utf-8 -*-
{
    'name': "Interview Assessment",

    'summary': """
        Interview Assessment Form 
        """,

    'description': """
        Interview Assessment Form 
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr', 'mail','hr_recruitment'],

    # always loaded
    'data': [
        'report/interview_assessment_report.xml',
        'report/interview_assessment_template.xml',
        'security/ir.model.access.csv',
        'views/interview_assessment_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
