# -*- coding: utf-8 -*-
{
    'name': "ds_purchase_track",

    'summary': """
        Add the tracking to purchase field. """,

    'description': """
        Add the tracking to purchase field. 
    """,

    'author': "Dashu-Tech",
    'website': "http://www.dashu-tech.com",
    'images': ['static/description/main_screenshot.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Purchase',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ds_mail_track', 'purchase'],

    "license": "AGPL-3",
    'installable': True,
    'support': 'lihaibin@dashu-tech.com',

}
