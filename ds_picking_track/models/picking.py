# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Picking(models.Model):
    _inherit = 'stock.picking'

    move_ids_without_package = fields.One2many('stock.move', 'picking_id', string="Stock moves not in package",
                compute='_compute_move_without_package', inverse='_set_move_without_package', tracking=True)

class StockMove(models.Model):
    _inherit = "stock.move"

    product_id = fields.Many2one(
        'product.product', 'Product',
        check_company=True, tracking=True,
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", index=True, required=True,
        states={'done': [('readonly', True)]})
    product_uom_qty = fields.Float(
        'Initial Demand', tracking = True,
        digits='Product Unit of Measure',
        default=0.0, required=True, states={'done': [('readonly', True)]},
        help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True, tracking = True,
                                  domain="[('category_id', '=', product_uom_category_id)]")

    state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')], string='Status',
        copy=False, default='draft', index=True, readonly=True, tracking = True,
        help="* New: When the stock move is created and not yet confirmed.\n"
             "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"
             "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to be manufactured...\n"
             "* Available: When products are reserved, it is set to \'Available\'.\n"
             "* Done: When the shipment is processed, the state is \'Done\'.")
