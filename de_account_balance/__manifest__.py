# -*- coding: utf-8 -*-
{
    'name': "Account Balance",

    'summary': """
    Display Account Balance
        """,

    'description': """
        this module will add account and balance in new field
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','account','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}