# -*- coding: utf-8 -*-
{
    'name': "Stock Restriction",

    'summary': """
           Stock Restriction 
           """,

    'description': """
       Stock Restriction 
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','mrp','sale','purchase'],

    # always loaded
    'data': [
        'data/operation_group.xml',
        'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}