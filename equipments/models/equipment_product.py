# -*- coding: utf-8 -*-
#import datetime
# import re
# import requests
# import socket
import logging

from odoo import api, fields, models, _
# from odoo.exceptions import UserError
# from odoo.tools import config, utc_to_shanghaitime, DEFAULT_SERVER_DATETIME_FORMAT
#
# from ..controllers.equipment_model import state_dict, empty, datetime2str
# from .import_feihang import ROUTING_URL

_logger = logging.getLogger(__name__)



class ProductEquipment(models.Model):
    _name = 'equipment.product.line'
    _description = "The equipment used by producing the product, and producing attributes"

    _sql_constraints = [('product_equipment_id_uniq', 'unique(main_product_id, equipment_id)', 'The equipment must be unique!')]

    main_product_id = fields.Many2one('equipment.product')
    category_id = fields.Many2one('maintenance.equipment.category', compute="_compute_category_id")
    equipment_id = fields.Many2one('maintenance.equipment', domain="[('category_id', '=', category_id)]")
    duration_per = fields.Integer(string="Duration Per Unit(s)", help="The seconds used to produce one unit of product with this equipment")

    def _compute_category_id(self):
        for p in self:
            cat = self.env['maintenance.equipment.category'].search([('workcenter_id', '=', p.main_product_id.workcenter_id.id)])
            p.category_id = cat[0] if cat else False


# 制造成品用到了哪些设备/模具
class MaintenanceProduct(models.Model):
    _name = 'equipment.product'
    _sql_constraints = [('product_id_uniq', 'unique(product_id)', 'The product must be unique!')]

    product_id = fields.Many2one('product.template', required=True)
    routing_id = fields.Many2one('mrp.routing', compute='_compute_product_routing', store=True)
    workcenter_id = fields.Many2one('mrp.workcenter', compute='_compute_product_routing')
    duration_per = fields.Integer(string="Default Duration(s)", help="The seconds used to produce one unit of product")
    equipment_line_ids = fields.One2many('equipment.product.line', 'main_product_id')
    # equipment_ids = fields.Many2many('maintenance.equipment', 'maintenance_product_equipment',
    #                                  domain="[('category_id.workcenter_id', '=', workcenter_id), ('equipment_model', '=', 'equipment')]",
    #                                  store=True)

    def name_get(self):
        return [(res.id, "[%s]%s" % (res.product_id.default_code, res.product_id.name)) for res in self]

    @api.depends('product_id')
    def _compute_product_routing(self):
        for res in self:
            res.routing_id = False
            res.workcenter_id = False
            if not res.product_id:
                continue
            bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', res.product_id.id), ('active', '=', True)])
            if bom_id:
                bom_id = bom_id[0]
                if bom_id.routing_id:
                    res.workcenter_id = bom_id.routing_id.mapped('operation_ids.workcenter_id')
                    res.routing_id = bom_id.routing_id

