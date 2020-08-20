# -*- coding: utf-8 -*-
{
    'name': "Finished Products",

    'summary': """
        Finished Products
        1-Manufacturing Order finish product
        """,

    'description': """
        Finished Products
        1-Manufacturing Order finish product pdf
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/mrp_finished_product.xml',
        'reports/mrp_finished_product_template.xml',
        'views/res_partner_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
