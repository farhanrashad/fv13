# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "PO Matrix Report",
    "category": 'Purchase',
    "summary": 'PO Matrix Report By Dynexcel',
    "description": """
	 This module is generating the pdf reports of the PO's matrix report.
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.0.0.0',
    "depends": ['sale','purchase'],
    "data": [
        'reports/po_matrix_report.xml',
        'reports/po_matrix_report_template.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}