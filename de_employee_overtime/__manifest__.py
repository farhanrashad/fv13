# -*- coding: utf-8 -*-
{
    'name': "Overtime Calculation",

    'summary': """
        Manages the Overtime for Employee based on Working Schedule.""",

    'description': """
        We have provided the feature that lets you make Salary Slip having the overtime 
        calculated as per the Working Schedule of the employee.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Overtime',
    'version': '13.0',

    'depends': ['base', 'hr', 'hr_payroll'],


    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_ext.xml',
        'views/employee_overtime.xml',
        'data/salary_rule_ext.xml',
        'views/payslip_ext.xml',
    ],
}
