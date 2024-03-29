# -*- coding: utf-8 -*-
# developed by Dashu-Tech

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def write(self, vals):
        if self.location_id.usage == 'internal' and 'quantity' in vals and \
                (vals['quantity'] < 0 and vals['quantity'] < self.quantity) and \
                'subcontract' not in self.product_id.bom_ids.mapped('type'):
            raise UserError(_("This will have product %s stock to be negative %f at location %s.") % \
                            (self.product_id.display_name, vals['quantity'], self.location_id.name))
        super(StockQuant, self).write(vals)
        return True

    @api.model
    def create(self, vals):
        loc = self.env['stock.location'].search([('id', '=', vals['location_id'])])
        prd = self.env['product.product'].search([('id', '=', vals['product_id'])])
        if loc.usage == 'internal' and 'quantity' in vals and (vals['quantity'] < 0 ) and \
                'subcontract' not in prd.bom_ids.mapped('type'):
            raise UserError(_("This will have product %s stock to be negative %f at location %s.") % \
                            (prd.display_name, vals['quantity'], loc.name))
        return super(StockQuant, self).create(vals)

