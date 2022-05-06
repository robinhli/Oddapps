# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Picking(models.Model):
    _inherit = 'stock.picking'

    move_ids_without_package = fields.One2many(tracking=True)


class StockMove(models.Model):
    _inherit = "stock.move"

    product_id = fields.Many2one(tracking=True)
    product_uom_qty = fields.Float(tracking=True)
    product_uom = fields.Many2one(tracking=True)

    state = fields.Selection(tracking=True)
