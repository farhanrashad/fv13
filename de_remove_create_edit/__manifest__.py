# -*- coding: utf-8 -*-

{
    "name": "Removeing Create and Edit",
    "category": 'Sale Order Purchase Order',
    "summary": 'removing create and edit option from so and po',
    "description": """
            This module will removing create and edit option from so and po
    """,
    "sequence": 2,
    "web_icon":"static/src/images/icon.png",
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.0.0.1',
    "depends": ['base','sale','purchase','account',],
    "data": [
        'views/remove_create_edit_po_so.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}



