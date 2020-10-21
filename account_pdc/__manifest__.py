# -*- coding: utf-8 -*-
{
    'name': 'PDC Management',
    'version': '1.0',
    'author': 'Dynexcel',
    'company': 'Dynexcel',
    'website': 'http://www.dynexcel.co',
    'category': 'Accounting',
    'summary': 'Extension on Cheques to handle Post Dated Cheques',
    'description': """ Extension on Cheques to handle Post Dated Cheques """,
    'depends': ['account_check_printing'],
    'data': [
        'data/account_pdc_data.xml',
        'views/account_payment_view.xml',
    ],
    'images': ['static/description/pdc_banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
