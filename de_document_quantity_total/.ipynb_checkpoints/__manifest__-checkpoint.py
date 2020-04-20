# -*- coding: utf-8 -*-
{
    'name': "Document Quantity Total",

    'summary': """
        Quantity Total for Documents include:
        - Purchase Order
        - Sale Order
        - Picking (Receipt/Transfer/Delivery Order)
        """,

    'description': """
        Quantity and Weight Total on Documents
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_views.xml',
        'views/sale_views.xml',
        'views/stock_picking_views.xml',
        'report/purchase_order_document_template.xml',
        'report/sale_order_document_template.xml',
        'report/delivery_slip_document_template.xml',
    ],
    "images":  ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
