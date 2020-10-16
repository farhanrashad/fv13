# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Report",

    'summary': """
            Helpdesk Ticket Report
            """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Reporting',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['report_xlsx','de_helpdesk'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'wizards/employee_attendance.xml',
        'report/employee_att_report.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
