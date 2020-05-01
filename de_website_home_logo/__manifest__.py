# -*- coding: utf-8 -*-
{
    'name': "Website Logo",

    'summary': """
    Homepage Logo
        """,

    'description': """
        Website Homepage Logo
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/website_views.xml',
        'views/website_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
