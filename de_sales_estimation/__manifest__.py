# -*- coding: utf-8 -*-
{
    'name': "Sales Estimation",

    'summary': """
        This app allow you to create sales estimate and send your customer by email along with sales estimate pdf report attached in mail.
         And it also allow you to create sales quotation directly from sales estimate.""",

    'description': """
        Sale Estimates to Customer
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/temp_sale_estimate.xml',
        'report/report.xml',
        'data/sequence.xml',
        'data/mail_template.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/sale_estimates.xml',
        'views/sale_menu.xml',
        'views/sale_order.xml',
        'views/crm_lead.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
