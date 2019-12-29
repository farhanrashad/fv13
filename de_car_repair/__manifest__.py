# -*- coding: utf-8 -*-
{
    'name': "Car Repair Management",

    'summary': """
    Car Repair Request, Car Diagnosis, Car Repair Job Order Management
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sales_team','sale','project','account',],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/car_repair_seq.xml',
        'views/menu_items.xml',
        'views/car_brand_views.xml',
        'views/car_category_views.xml',
        'views/car_views.xml',
        'views/product_views.xml',
        'views/car_repair_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
