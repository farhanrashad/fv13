# -*- coding: utf-8 -*-
{
    'name': "Gain Report",

    'summary': """
                Sale Gain Report
                """,

    'description': """
        Sale Gain Report
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Training',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'sale','purchase','account'],

    # always loaded
    'data': [
        'report/sale_gain_report.xml',
        'report/sale_gain_report_template.xml',
        'views/sale_gain_views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
