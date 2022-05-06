# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpBom(models.Model):
    _name = 'mrp.bom'
    _inherit = ['mrp.bom', 'mail.thread', 'mail.activity.mixin']

    bom_line_ids = fields.One2many(tracking=True)


class MrpBOMLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_id = fields.Many2one(tracking=True)
    product_qty = fields.Float(tracking=True)
    product_uom_id = fields.Many2one(tracking=True)
    operation_id = fields.Many2one(tracking=True)

