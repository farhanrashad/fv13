# -*- coding: utf-8 -*-
{
    'name': "Sale Mrp Properties",

    'summary': """
        Sale Production Properties""",

    'description': """
        Sale Mrp Properties
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Sale Mrp',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/property_set.xml',
        'views/production_properties.xml',
        'views/mrp_production.xml',
        'views/mrp_production_template_ext.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
