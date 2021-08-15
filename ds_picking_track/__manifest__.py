# -*- coding: utf-8 -*-
{
    'name': "ds_picking_track",

    'summary': """
        Add tracking to picking/move field""",

    'description': """
        Add tracking to picking/move field
    """,

    'author': "Dashu-Tech",
    'website': "http://www.dashu-tech.com",
    'images': ['static/description/main_screenshot.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['ds_mail_track', 'stock'],

    "license": "AGPL-3",
    'support': 'lihaibin@dashu-tech.com',

}