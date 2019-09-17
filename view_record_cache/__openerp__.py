# -*- coding: utf-8 -*-
{
    'name': "Ir Ui View Cache",

    'summary': """
       Use this module to accelerate the load""",

    'description': """
        This module saves the requests of the ir.ui.view object record
        s in the cache which is a high speed data storage layer V8
    """,

    'author': "JUVENTUD PRODUCTIVA VENEZOLANA",
    'website': "http://www.juventudproductivabicentenaria.com",
    'category': 'Performance',
    'version': '0.1',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv'
    ],
    'demo': [],
    'images': ['static/images/view_cache_screenshot.png'],
    'application': True,
    'installable': True,
   
}
