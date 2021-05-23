# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv.query import Query

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_spec = fields.Char("Product Specification")

    def name_get(self):
        res = super(ProductTemplate, self).name_get()
        self.sudo().read(['product_spec'], load=False)

        new_res = []
        for p, product in zip(res, self.sudo()):
            new_res.append((p[0], '%s [%s]' % (p[1], product.product_spec)))
        return new_res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        res = super(ProductTemplate, self)._name_search(name, args, operator, limit, name_get_uid)
        if name:
            if not args:
                args = []
            res_spec_ids = self._search([('product_spec', 'ilike', name)] + args, limit=limit, access_rights_uid=name_get_uid)
            res_spec = self.browse(res_spec_ids).ids
            res = self.browse(res).ids
            res_spec = set(res_spec) - set(res)
            res_spec = list(res_spec)
            return res + res_spec
        return res

class Product(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        res = super(Product, self).name_get()
        self.sudo().read(['product_spec'], load=False)

        new_res = []
        for p, product in zip(res, self.sudo()):
            new_res.append((p[0], '%s [%s]' % (p[1], product.product_spec)))
        return new_res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        res = super(Product, self)._name_search(name, args, operator, limit, name_get_uid)
        if name:
            if not args:
                args = []
            res_spec_ids = self._search([('product_spec', 'ilike', name)] + args, limit=limit, access_rights_uid=name_get_uid)
            res_spec = self.browse(res_spec_ids).ids
            res = self.browse(res).ids
            res_spec = set(res_spec) - set(res)
            res_spec = list(res_spec)
            return res + res_spec
        return res

