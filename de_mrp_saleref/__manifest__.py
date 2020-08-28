# -*- coding: utf-8 -*-
{
    'name': "Sale Reference",

    'summary': """
                Sale Reference in Manufacturing order
                """,

    'description': """
        Hr Training Program- This Module will provide all the information related to courses and session in the training program.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Training',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'sale'],

    # always loaded
    'data': [
        'views/mrp_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
