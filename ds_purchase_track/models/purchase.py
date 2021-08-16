# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Purchaes(models.Model):
    _inherit = 'purchase.order'

    order_line = fields.One2many('purchase.order.line', 'order_id', string='Order Lines', tracking=True,
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, tracking=True)
    date_planned = fields.Datetime(string='Scheduled Date', index=True, tracking=True)
    taxes_id = fields.Many2many('account.tax', string='Taxes', tracking=True, domain=['|', ('active', '=', False), ('active', '=', True)])
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', tracking=True, domain="[('category_id', '=', product_uom_category_id)]")
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True, tracking=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price', tracking=True)
