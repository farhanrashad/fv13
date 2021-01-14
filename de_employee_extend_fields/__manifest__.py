# -*- coding: utf-8 -*-
{
    'name': "Employee Extend Fields",

    'summary': """
        Employee Extend Feilds and emergency contact details""",

    'description': """
        Long description of module's purposes
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Hr',
    'version': '13.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

}