# -*- coding: utf-8 -*-
{
    'name': "User Restriction",

    'summary': """
        Disable user right to create customer/vendor
        """,

    'description': """
        Disable user right to create customer/vendor for user
        1-Awais
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','purchase','sale'],

    # always loaded
    'data': [
#         'security/security.xml',
#         'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
