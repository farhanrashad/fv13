# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Changes in Peroforma Invoice",
    "category": 'Sale',
    "summary": 'Change in Peroforma Invoice in sale order',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.0',
    "depends": ['base','sale'],
    "data": [
        'security/ir.model.access.csv',
        'report/performa_invoice_report_inh.xml',
        'report/performa_invoice_report_pdf.xml',
        'views/performa_invoice_view_inh.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
