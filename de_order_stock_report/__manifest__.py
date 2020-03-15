# -*- coding: utf-8 -*-
{
    'name': "Order Stock Report",

    'summary': """
    Order wise Stock Report
        """,

    'description': """
Order Wise Stock Report
""",

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','de_job_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/order_stock_wizard_view.xml',
        'views/stock_report_menu_views.xml',
        'report/order_stock_template.xml',
        'report/order_stock_report.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
