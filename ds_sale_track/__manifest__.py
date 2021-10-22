# -*- coding: utf-8 -*-
{
    'name': "ds_sale_track",

    'summary': """
        Add tracking to sale order and line fields to track the sale order line change""",

    'description': """
        Add tracking to sale order and line fields to track the sale order line change
    """,

    'author': "Dashu-Tech",
    'website': "http://www.dashu-tech.com",
    'images': ['static/description/main_screenshot.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ds_mail_track', 'sale'],
    "license": "LGPL-3",
    'support': 'lihaibin@dashu-tech.com',

}