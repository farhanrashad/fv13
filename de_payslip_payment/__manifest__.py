# -*- coding: utf-8 -*-
{
    'name': "Payslip Payment",

    'summary': """
    Generate Payment
        """,

    'description': """
        Generate Payment
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '11.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_payroll','account_batch_deposit','account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_batch_payment.xml',
        'views/hr_employee_views.xml',
        'views/hr_payslip_run_views.xml',
        'views/hr_payslip_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
