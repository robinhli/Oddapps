# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    qty_available_no_defects = fields.Float(
        'Quantity No Defects', compute='_compute_quantities_no_defects', search='_search_qty_available_no_defects',
        digits=dp.get_precision('Product Unit of Measure'),
        help="Current quantity of products with no defects.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def _compute_quantities_no_defects(self):
        res = self.with_context(no_defects=True)._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date'))
        for product in self:
            product.qty_available_no_defects = res[product.id]['qty_available']

    def _search_qty_available_no_defects(self, operator, value):
        # In the very specific case we want to retrieve products with stock available, we only need
        # to use the quants, not the stock moves. Therefore, we bypass the usual
        # '_search_product_quantity' method and call '_search_qty_available_new' instead. This
        # allows better performances.
        if value == 0.0 and operator == '>' and not ({'from_date', 'to_date'} & set(self.env.context.keys())):
            product_ids = self.with_context(no_defects=True)._search_qty_available_new(
                operator, value, self.env.context.get('lot_id'), self.env.context.get('owner_id'),
                self.env.context.get('package_id')
            )
            return [('id', 'in', product_ids)]
        return self._search_product_quantity(operator, value, 'qty_available_no_defects')

    # for function of not including defects in qty_in_hand
    def _get_domain_locations(self):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = super(ProductProduct, self)._get_domain_locations()
        if self._context.get("no_defects", False):
            defects_locations = self.env['stock.location'].search([('defects', '=', True)])
            if defects_locations:
                domain_quant_loc += [('location_id', 'not in', defects_locations.ids)]
        return domain_quant_loc, domain_move_in_loc, domain_move_out_loc

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_available_no_defects = fields.Float(
        'Quantity On Hand', compute='_compute_quantities_no_defects', search='_search_qty_available_no_defects',
        digits=dp.get_precision('Product Unit of Measure'))

    def _compute_quantities_no_defects(self):
        res = self.with_context(no_defects=True)._compute_quantities_dict()
        for template in self:
            template.qty_available_no_defects = res[template.id]['qty_available']
