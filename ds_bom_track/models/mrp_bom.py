# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpBom(models.Model):
    _name = 'mrp.bom'
    _inherit = ['mrp.bom', 'mail.thread', 'mail.activity.mixin']

    bom_line_ids = fields.One2many('mrp.bom.line', 'bom_id', 'BoM Lines', copy=True, tracking=True)

class MrpBOMLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_id = fields.Many2one( 'product.product', 'Component', required=True, check_company=True, tracking=True)
    product_qty = fields.Float('Quantity', default=1.0,
        digits='Product Unit of Measure', required=True, tracking=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        # default=_get_default_product_uom_id,
        required=True, tracking=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control", domain="[('category_id', '=', product_uom_category_id)]")

    operation_id = fields.Many2one(
        'mrp.routing.workcenter', 'Consumed in Operation', check_company=True, tracking=True,
        domain="[('routing_id', '=', routing_id), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        help="The operation where the components are consumed, or the finished products created.")
