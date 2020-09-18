# -*- coding: utf-8 -*-
{
    'name': "equipments",

    'summary': """
        Add equipments under workcenter and and equipment_id to 
        workorder and production""",

    'description': """
        Add equipments under workcenter and and equipment_id to 
        workorder and production. Users can assign the different 
        equipment to different production/workorder.
    """,

    'author': "Dashu-Tech",
    'website': "http://www.dashu-tech.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['maintenance', 'mrp'],
    'images': ['static/description/main_screenshot.png',
               'static/description/Equipment.png',
               'static/description/Equipment_category.png',
               'static/description/Product_equipment.png',
               'static/description/WO_equipment.png',
               ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_category_views.xml',
        'views/maintenance_equipment_views.xml',
        'views/mrp_production_views.xml',
        'views/product_maintenance_views.xml',
        'views/mrp_workorder_views.xml',
    ],
    "license": "AGPL-3",
}
