# -*- coding: utf-8 -*-
{
    'name': "Product Weight",

    'summary': """
    Stock & Billing
        """,

    'description': """
        Product Weight
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '1.3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','sale','purchase','mrp','de_product_dimensions'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_views.xml',
        'views/picking_views.xml',
        'views/mrp_views.xml',
        'views/sale_views.xml',
		'views/product_views.xml',
        'views/partner_views.xml',
        'views/stock_production_lot_views.xml',
        'views/stock_quant_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}