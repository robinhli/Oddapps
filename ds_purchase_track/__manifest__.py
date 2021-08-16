# -*- coding: utf-8 -*-
{
    'name': "ds_purchase_track",

    'summary': """
        Add the tracking to purchase field. Free download at https://github.com/robinhli/Oddapps""",

    'description': """
        Add the tracking to purchase field. 
    """,

    'author': "Dashu-Tech",
    'website': "http://www.dashu-tech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ds_mail_track', 'purchase'],
    'images': ['static/description/main_screenshot.png'],
    "license": "LGPL-3",
    'support': 'lihaibin@dashu-tech.com',

}