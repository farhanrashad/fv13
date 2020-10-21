# -*- coding: utf-8 -*-
{
    'name': 'PDC Payments Report',
    'version': '11.0.2.0',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'http://www.cybrosys.com',
    'category': 'Accounting',
    'summary': 'Report of Payments with filter for PDC type',
    'description': """ Report of Payments with filter for PDC type """,
    'depends': ['account_check_printing', 'account_pdc'],
    'data': [
        'views/report_payment.xml',
        'wizard/account_report_payment_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
