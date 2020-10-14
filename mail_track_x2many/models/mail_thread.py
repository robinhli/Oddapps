# -*- coding: utf-8 -*-
# Part of DashuMom. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _, tools

from odoo.tools.float_utils import float_compare
import copy
import logging
from odoo.addons import decimal_precision as dp
from datetime import datetime


_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    '''
    this inherit add the track ability for one2many fields.
    Need to set track_visibility of the related filed to any of 'onchange' or 'alyways', such as 'order_line' at purchase order
    Then set the filed of submodel such as 'purchase.order.line', so the finally actually put the change of submodel.
    '''
    _inherit = 'mail.thread'

    @api.model
    def _get_tracked_fields(self, updated_fields):
        """ Return a structure of tracked fields for the current model.
            :param list updated_fields: modified field names
            :return dict: a dict mapping field name to description, containing
                always tracked fields and modified on_change fields
        """
        tracked_fields =  super(MailThread, self)._get_tracked_fields(updated_fields)
        # tracked_fields = {key: tracked_fields[key] for key in set(updated_fields) & set(list(tracked_fields)) }
        for t in tracked_fields:
            if tracked_fields[t]['type'] == 'one2many':
                sub_tracked_fields = self._get_sub_tracked_fields(tracked_fields[t]['relation'],
                                                                  tracked_fields[t]['relation_field'])
                if sub_tracked_fields:
                    tracked_fields[t]['tracked_fields'] = sub_tracked_fields
        return tracked_fields


    def _get_sub_tracked_fields(self, model, inverse_name):
        tracked_fields = []
        for name, field in self.env[model]._fields.items():
            if getattr(field, 'track_visibility', False):
                if getattr(field, 'related') == None or (getattr(field, 'related') != None and
                                                                 getattr(field, 'related', False)[0] != inverse_name):
                    tracked_fields.append(name)
        if tracked_fields:
            # tracked_fields.append('name')
            tracked_fields.append(self.env[model]._rec_name)
            return self.env[model].fields_get(tracked_fields)
        return {}

    def get_initial_values(self, tracked_fields):
        initial_values = dict((record.id, dict((key, getattr(record, key)) for key in tracked_fields))
                              for record in self)
        for t in tracked_fields:
            if tracked_fields[t]['type'] == 'one2many':
                # sub_tracked_fields = self._get_sub_tracked_fields(tracked_fields[t]['relation'],
                #                                                   tracked_fields[t]['relation_field'])
                # tracked_fields[t]['tracked_fields'] = sub_tracked_fields
                for rec in initial_values:
                    initial_values[rec][t] = dict(
                        (record.id, dict((key, getattr(record, key)) for key in tracked_fields[t]['tracked_fields']))
                        for record in initial_values[rec][t])
        return initial_values

    @api.multi
    def _message_track(self, tracked_fields, initial):
        displays = set()  # contains always tracked field that did not change but displayed for information
        display_values_ids = []
        tracked_fields_no_sub = dict.copy(tracked_fields)
        initial_no_sub = dict.copy(initial)
        for col_name, col_info in tracked_fields.items():
            if col_info['type'] == 'one2many':
                del tracked_fields_no_sub[col_name]
                del initial_no_sub[col_name]
        changes, tracking_value_ids = super(MailThread, self)._message_track(tracked_fields_no_sub, initial_no_sub)

        for col_name, col_info in tracked_fields.items():
            initial_value = initial[col_name]
            new_value = getattr(self, col_name)
            if 'related' in col_info:
            #     skipthis = False
            #     for f in col_info['related']:
                if getattr(self._fields[col_info['related'][0]], 'type') == 'one2many':
                    skipthis = True
            #             break
            #     if skipthis == True:
                    continue
            if col_info['type'] != 'one2many':
                continue
            new_value = dict((record.id, dict((key, getattr(record, key)) for key in col_info['tracked_fields']))
                              for record in new_value)
            if initial_value:
                deletedlines = set(initial_value) - set(new_value)
                for delline in deletedlines:
                    if 'name' in initial_value[delline]:
                        subname = initial_value[delline]['name']
                    elif 'product_id' in initial_value[delline]:
                        subname = initial_value[delline]['product_id'].display_name
                    else:
                        if getattr(self, col_name)._rec_name:
                            subname = getattr(initial_value[delline][getattr(self, col_name)._rec_name],
                                              initial_value[delline][getattr(self, col_name)._rec_name]._rec_name)
                        else:
                            subname = str(delline)
                    try:
                        subname = subname[: subname.index(']') + 1]
                    except ValueError:
                        pass
                    values = {'field': col_name, 'field_desc': _('%s.Deleted.%s') % (col_info['string'], subname),
                        'field_type': col_info['type']}
                    tracking_value_ids.append([0, 0, values])
                    changes.add(col_name)
            for record in new_value:
                subname = getattr(self, col_name).filtered(lambda x: x.id == record)
                if 'name' in subname:
                    subname=subname.name
                else:
                    subname=subname.display_name
                try:
                    subname.index(']')
                    subname = subname[: subname.index(']') + 1]
                except ValueError:
                    pass
                if not initial_value or record not in initial_value.keys():
                    # there are no initial value for the record, so it's a newly added line
                    values = {'field': col_name, 'field_desc': _('%s.Added.%s') % (col_info['string'], subname),
                        'field_type': col_info['type']}
                    tracking_value_ids.append([0, 0, values])
                    changes.add(col_name)
                    continue

                for subcol_name, subcol_info in col_info['tracked_fields'].items():
                    subnew_value = new_value[record][subcol_name]
                    subinitial_value = initial_value[record][subcol_name]
                    subtrack_visibility = getattr(self.env[col_info['relation']]._fields[subcol_name], 'track_visibility', 'onchange')
                    track_sequence = getattr(self._fields[col_name], 'track_sequence', 100)
                    if subnew_value != subinitial_value and (subnew_value or subinitial_value):  # because browse null != False
                        tracking = self.env['mail.tracking.value'].create_tracking_values(subinitial_value, subnew_value,
                                                                                          subcol_name, subcol_info, track_sequence)
                        if tracking:
                            tracking['field_desc'] = '%s.%s.%s' % (col_info['string'], subname, tracking['field_desc'])
                            tracking_value_ids.append([0, 0, tracking])

                        if subcol_name in col_info['tracked_fields']:
                            changes.add(col_name)
                    # 'always' tracked fields in separate variable; added if other changes
                    elif subnew_value == subinitial_value and subtrack_visibility == 'always' and subcol_name in col_info['tracked_fields']:
                        tracking = self.env['mail.tracking.value'].create_tracking_values(subinitial_value,
                                                                                          subinitial_value, subcol_name,
                                                                                          subcol_info, track_sequence)
                        if tracking:
                            tracking['field_desc'] = '%s.%s.%s' % (col_info['string'], subname, tracking['field_desc'])
                            display_values_ids.append([0, 0, tracking])
                            displays.add(col_name)

        if changes and displays:
            tracking_value_ids = display_values_ids + tracking_value_ids
        self._process_varchar(tracking_value_ids)
        return changes, tracking_value_ids

    def _process_varchar(self, tracking_value_ids):
        for rec in tracking_value_ids:
            if rec[2]['field_type'] == 'char':
                new_value = rec[2]['new_value_char'] and rec[2]['new_value_char'].split(',')
                old_value = rec[2]['old_value_char'] and rec[2]['old_value_char'].split(',')
                if not (new_value and old_value):
                    continue
                new_value = set(item.strip() for item in new_value)
                old_value = set(item.strip() for item in old_value)
                added = set(new_value) - set(old_value)
                deleted = set(old_value) - set(new_value)
                if added:
                    rec[2]['new_value_char'] = 'Added: %s' % str(added).replace("'", '')
                else:
                    rec[2]['new_value_char'] = ''
                if deleted:
                    rec[2]['old_value_char'] = 'Deleted: %s' % str(deleted).replace("'", '')
                else:
                    rec[2]['old_value_char'] = ''
