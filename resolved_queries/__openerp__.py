# -*- coding: utf-8 -*-
{
    'name': "See Resolved Queries",

    'summary': """
        See resolved queries made to postgresql to measure performance.""",

    'description': """
        See resolved queries made to postgresql to measure performance.
    """,

    'author': "JUVENTUD PRODUCTIVA BICENTENARIA",
    'website': "http://www.juventudproductivabicentenaria.com",
    'category': 'Extra Tool',
    'version': '0.1',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'security/query_security.xml',
        'views/resolved_queries.xml',
        'wizard/run_resolved_queries.xml',
        'wizard/data_resolved_queries.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/images/resolved_queries_screenshot.gif']
}

