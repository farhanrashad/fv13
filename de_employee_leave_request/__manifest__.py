# -*- coding: utf-8 -*-
{
    'name': "Employee Leave Request",

    'summary': """
        Leave Request Functionality for portal user.""",

    'description': """
        Leave Request Functionality for portal user.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Helpdesk',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'hr', 'hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/groups.xml',
        'views/website_assets.xml',
        'views/website_page.xml',
        'views/website_ext.xml',
        'views/leave_request_template.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
