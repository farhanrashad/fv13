# -*- coding: utf-8 -*-
{
    'name': "Advance Salary",

    'summary': """
          Employee Advance Salary
          """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail','account'],

    # always loaded
    'data': [
        'data/salary_seq.xml',
        'report/advance_salary_report.xml',
        'report/advance_salary_template.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
