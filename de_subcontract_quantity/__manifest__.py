# -*- coding: utf-8 -*-
{
    'name': "Purchase Subcontracting Quantity",

    'summary': """
    Purchase Subcontracting Quantity
        """,

    'description': """
        Purchase Subcontracting Quantity
    """,

    'author': "Dynexcel",
    'website': "http://www.Dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','mrp','purchase','de_job_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
