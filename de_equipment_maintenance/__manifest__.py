# -*- coding: utf-8 -*-
{
    'name': "Equipment Maintenance",

    'summary': """
    extend maintenance module functionality
        """,

    'description': """
        parts and services in maintenace
    """,

    'author': "Dynexcel",
    'website': "http://www.Dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','maintenance','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/em_order_seq.xml',
        'data/maintenance_data.xml',
        'views/equipment_views.xml',
        'views/em_order_views.xml',
        'views/maintenance_views.xml',
        'views/stock_move_views.xml',
        'reports/maintenance_reports.xml',
        'reports/pm_templates_pm_order_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
