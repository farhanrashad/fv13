# -*- coding: utf-8 -*-
{
    'name': "PO Generation from MOs",

    'summary': """
           PO Generation from MOs
           """,

    'description': """
           PO Generation from MOs
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','purchase','sale'],

    # always loaded
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
#         'wizard/mo_wizard_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
