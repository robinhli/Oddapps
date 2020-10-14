# -*- coding: utf-8 -*-
{
    'name': "mail_track_x2many",

    'summary': """
        Track One2Many and Many2Many change.""",

    'description': """
        Track One2Many and Many2Many change.
        The value change of one2many or many2many fields change
        can be tracked as the normal fields, provide you define
        the fields as tracking. (set track_visibility='always', 
        or 'onchange') if it's one2many, need to set the one2many
        field itself and the sub-field at many sub-table.
    """,

    'author': "Dashu Tech",
    'website': "http://www.dashu-tech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'support': 'lihaibin@dashu-tech.com',
    'price': 99,
    'currency': 'EUR',
}