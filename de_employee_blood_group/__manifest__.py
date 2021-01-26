# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Blood Group",
    "category": 'HR',
    "summary": 'Employee Blood Group',
    "description": """
	 This module adds the functionality of blood group in the employee form
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.0.0.0',
    "depends": ['base', 'hr'],
    "data": [
        'views/blood_group_view.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
