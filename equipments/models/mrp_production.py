# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api,_

_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")
