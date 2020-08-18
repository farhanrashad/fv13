# -*- coding: utf-8 -*-
{
    'name': "Open HRMS Employee Shift",
    'version': '13.0.1.0.0',
    'summary': """Easily create, manage, and track employee shift schedules.""",
    'description': """Easily create, manage, and track employee shift schedules.""",
    'category': 'Human Resource',
    'author': 'Dynexcel',
    'website': "https://www.dynexcel.co",
    'depends': ['hr', 'hr_payroll', 'resource'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_employee_shift_security.xml',
        'views/hr_employee_shift_view.xml',
        'views/hr_employee_contract_view.xml',
        'views/hr_generate_shift_view.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/shift_schedule_data.xml',
    ],
    'images': ["static/description/banner.png"],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
