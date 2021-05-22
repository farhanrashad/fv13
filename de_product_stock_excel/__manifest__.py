# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Product XLSX Report",
    "category": 'Education',
    "summary": 'Product Report Summary',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '11.0',
    "depends": ['sale'],
    "data": [
        # 'security/ir.model.access.csv',
        'views/product_stock_excel_report_view.xml',
        'reports/product_stock_excel_report_pdf.xml',
        'reports/product_stock_excel_card.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}