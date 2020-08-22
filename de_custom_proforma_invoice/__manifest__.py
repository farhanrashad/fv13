# -*- coding: utf-8 -*-
{
    'name': "Custom Proforma Invoice",

    'summary': """
        Custom proforma invoices for particular customers.""",

    'description': """
        This module will modify custom proforma invoices.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/custom_files.xml',
        'wizard/custom_proforma_invoice1.xml',
        'views/sale_order_ext.xml',
        'views/product_ext.xml',
        'views/report_action.xml',
        'report/custom_proforma_template1.xml',
        'report/layouts.xml',
    ],
}
