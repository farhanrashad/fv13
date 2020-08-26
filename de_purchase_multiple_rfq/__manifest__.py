# -*- coding: utf-8 -*-
{
    'name': "Multiple RFQs",

    'summary': """
        Purchase Multiple RFQs
        """,

    'description': """
        Purchase Multiple RFQs
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','purchase','sale'],

    # always loaded
    'data': [
        'report/purchase_demand_report.xml',
        'report/demand_report_template.xml',
        'data/data_seq_views.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
