# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_line = fields.One2many(tracking=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_unit = fields.Float(tracking=True)
    tax_id = fields.Many2many(tracking=True)
    product_id = fields.Many2one(tracking=True)
    product_uom_qty = fields.Float(tracking=True)
    product_uom = fields.Many2one(tracking=True,)
