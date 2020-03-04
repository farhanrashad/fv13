# -*- coding: utf-8 -*-
{
    'name': "Order Approval",

    'summary': """
    Order approval
        """,

    'description': """
        add validation on sales order
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'sales_team'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_approval_reason_view.xml',
        'views/res_users_views.xml',
        'views/sale_views.xml',
        'data/mail_template.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
