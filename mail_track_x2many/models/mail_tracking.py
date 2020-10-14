# -*- coding: utf-8 -*-
# Part of DashuMom. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _, tools

from odoo.tools.float_utils import float_compare
import copy
import logging
from odoo.addons import decimal_precision as dp
from datetime import datetime


_logger = logging.getLogger(__name__)

class MailTracking(models.Model):
    _inherit = 'mail.tracking.value'

    @api.model
    def create_tracking_values(self, initial_value, new_value, col_name, col_info, track_sequence):
        values = {'field': col_name, 'field_desc': col_info['string'], 'field_type': col_info['type'], 'track_sequence': track_sequence}
        if col_info['type'] == 'many2many':
            values.update({
                # 'old_value_integer': initial_value and initial_value.ids or 0,
                # 'new_value_integer': new_value and new_value.ids or 0,
                'old_value_char': initial_value and [y for x, y in initial_value.name_get()] or ' ',
                'new_value_char': new_value and [y for x, y in new_value.name_get()] or ' '
            })
            return values
        else:
            return super(MailTracking, self).create_tracking_values(initial_value, new_value, col_name, col_info, track_sequence)

