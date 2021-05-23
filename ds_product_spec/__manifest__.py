# -*- coding: utf-8 -*-
{
    'name': "ds_product_spec",

    'summary': """
        Add a new field of product specification to product template, and show it on name
        with [default_code]name[product_spec] style and can be searched""",

    'description': """
        Add a new field of product specification to product template, and show it on name
        with [default_code]name[product_spec] style and can be searched
    """,

    'author': "Dashu-Tech",
    'website': "http://www.dashu-tech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    "version": "14.0.1.0.1",

    # any module necessary for this one to work correctly
    'depends': ['product'],
    'images': ['static/description/main_screenshot.png', 'static/description/screenshot_1.png'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
    ],
    "license": "AGPL-3",
}