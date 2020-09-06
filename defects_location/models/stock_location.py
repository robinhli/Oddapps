# -*- coding: utf-8 -*-
# Part of Dashu. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = "stock.location"
    defects = fields.Boolean("Defects Products", default = False,
            help="True for not conforming products(defects), False for default. For internal usage location only")
    # to_be_checked = fields.Boolean("To Be Checked", help = "To Be Checked Location. Will not be in valued stock")
