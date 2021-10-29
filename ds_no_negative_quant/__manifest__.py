# -*- coding: utf-8 -*-
{
    'name': "ds_no_negative_quant",

    'summary': """
        不允许实体库位的负库存。如果已经有负库存，只能减少负库存数量或者变为0，正库存，不能增加负库存数量""",

    'description': """
        不允许实体库位的负库存。如果已经有负库存，只能减少负库存数量或者变为0，正库存，不能增加负库存数量
    """,

    'author': "Dashu-Tech",
    'website': "http://www.dashu-tech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Operations/Inventory',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    "license": "AGPL-3",
}