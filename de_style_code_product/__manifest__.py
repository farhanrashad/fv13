# -*- coding: utf-8 -*-
{
    'name': "Adding New Field in Product Template",

    'summary': """ This module will add a field in product template and in search view""",

    'description': """ This module will add a field in product.template and in search view """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Employee',
    'version': '13.0.0.0',



    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'views/style_code_product_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

