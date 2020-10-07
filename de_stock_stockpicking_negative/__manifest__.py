# -*- coding: utf-8 -*-
{
    'name': "Disable Negative Stock",

    'summary': """
        Disable Negative Stock.""",

    'description': """
        Disable validation of receipt before validation of delivery order.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
}
