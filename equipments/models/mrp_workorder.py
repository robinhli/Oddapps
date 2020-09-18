# -*- coding: utf-8 -*-
# Part of Dashu-Tech. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    equipment_id = fields.Many2one('maintenance.equipment', related='production_id.equipment_id',
                                   store=True)
