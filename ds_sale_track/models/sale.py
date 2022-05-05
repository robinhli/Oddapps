# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines',
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                 copy=True, auto_join=True, tracking=True)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0, tracking=True)

    tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)],
                              tracking=True)

    product_id = fields.Many2one(
        'product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True, tracking=True)  # Unrequired company

    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True,
                                   default=1.0, tracking=True)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', tracking=True,
                                  domain="[('category_id', '=', product_uom_category_id)]")

    def track_display(self):
        self.ensure_one()
        return "%s, %s, %s" % (self.product_id.display_name, self.product_uom_qty, self.product_uom.name)
