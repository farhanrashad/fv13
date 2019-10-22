# -*- coding: utf-8 -*-
{
    'name': "Print Reports",

    'summary': """
    Print Reports Enhacement
        """,

    'description': """
        Add fields in print reports
        1. Sale Order
        2. Performa Invoice
        3. Invoice
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/saleorder_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/templates.xml',
        'views/saleorder_report_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}