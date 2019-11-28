# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################
{
    'name': 'Product Ledger',
    'version': '1.1',
    'summary': 'Product Ledger Report',
    'description': 'This module provides the movement of individual products with opening and closing stocks',
    'author': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'company': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'depends': ['stock'],
    'category': 'Inventory',
    'demo': [],
    'data': ['views/product_ledger_views.xml',
             'security/ir.model.access.csv',
             'report/product_ledger_report.xml',
             'report/product_ledger_report_template.xml'],
    'installable': True,
    'images': ['static/description/banner.png'],
    'qweb': [],
    'license': "Other proprietary",
    'auto_install': False,
    'price':29.0,
    'currency':'EUR',
    'live_test_url':'https://youtu.be/5OqXXKO6gRA',
}
