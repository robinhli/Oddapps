# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Purchaes(models.Model):
    _inherit = 'purchase.order'

    order_line = fields.One2many(tracking=True)


class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    product_qty = fields.Float(tracking=True)
    date_planned = fields.Datetime(tracking=True)
    taxes_id = fields.Many2many(tracking=True)
    product_uom = fields.Many2one(tracking=True)
    product_id = fields.Many2one(tracking=True)
    price_unit = fields.Float(tracking=True)
