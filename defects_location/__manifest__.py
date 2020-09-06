# -*- coding: utf-8 -*-
{
    'name': "defects_location",

    'summary': """
        不合格品位置""",

    'description': """
        仓库位置的属性里增加一个不合格品打勾的属性，打勾后表示不合格品。缺省不打勾表示合格品。
        在产品/产品变体页面原“在手”按钮前增加一个按钮表示“在手合格品”
        库存页面，增加筛选“合格品区”，“不合格品区”
    """,

    'author': "Dashu Tech",
    'website': "http://www.dashu-tech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    "version": "11.0.1.0.1",

    # any module necessary for this one to work correctly
    'depends': ['stock'],
    'images':  ['static/images/main_screenshot.png', 'static/images/main_1.png', 'static/images/main_2.png'],


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/stock_location_views.xml',
        'views/stock_quant_views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    "license": "AGPL-3",
}