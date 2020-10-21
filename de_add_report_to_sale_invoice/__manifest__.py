# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo 13 Accounting Add A Report To Sale Invoice',
    'version': '13.0.1.1.2',
    'category': 'Invoicing Management',
    'summary': 'Add a Report to Sale invoice',
    'sequence': '10',
    'author': 'Odoo Mates, Odoo SA',
    'license': 'LGPL-3',
    'company': 'Odoo Mates',
    'maintainer': 'Odoo Mates',
    'support': 'odoomates@gmail.com',
    'website': 'http://odoomates.tech',
    'depends': ['account'],
    'live_test_url': 'https://www.youtube.com/watch?v=Qu6R3yNKR60',
    'demo': [],
    'data': [
        'reports/report_delivery_note.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
    'qweb': [],
}
