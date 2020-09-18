# -*- coding: utf-8 -*-
import datetime
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


# 设备/模具类别
class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    workcenter_id = fields.Many2one('mrp.workcenter')



class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    _order = 'name'

    _sql_constraints = [('serial_no_uniq', 'unique(serial_no)', 'The serial no must be unique!')]

    def _get_equipment_model_id(self):
        MT = self.env['maintenance.equipment.category']
        team = MT.search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if not team:
            team = MT.search([], limit=1)
        return team.id

    state = fields.Selection([
        ('run', _('run')),
        ('free', _('free')),
        ('repair', _('repair')),
        ('pm_maintain', _('pm_maintain')),
        ('inside_maintain', _('inside_maintain')),
        ('outside_maintain', _('outside_maintain')),
        ('outside_help', _('outside_help')),
    ], default='free')
    workorder_number = fields.Integer(compute='_compute_workorder_number')
    # serial_no = fields.Char('Serial Number', copy=False, readonly=True, default=lambda x: _('New'))

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name + ('/' + record.serial_no) if record.serial_no else ''))

        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('serial_no', operator, name)]
        pos = self.search(domain + args, limit=limit)
        return pos.name_get()

    def _compute_workorder_number(self):
        workorder_ids = self.env['mrp.workorder'].search([('equipment_id', '=', self.id)])
        self.workorder_number = len(workorder_ids)

    def action_equipment_used(self):
        self.ensure_one()
        action = self.env.ref('mrp.action_mrp_workorder_workcenter').read()[0]
        action['domain'] = [('equipment_id', '=', self.id)]
        # elif self.equipment_model == 'model':
        #     action['domain'] = [('model_actual_id', '=', self.id)]
        return action


    def return_state(self):
        return self.state

    def _create_maintain_request(self, date, duration):
        self.ensure_one()
        self.env['maintenance.request'].create({
            'name': _('Preventive Maintenance - %s') % self.name,
            'request_date': date,
            'category_id': self.category_id.id,
            'equipment_id': self.id,
            'repair_maintain': 'maintain',
            'maintenance_type': 'preventive',
            'owner_user_id': self.owner_user_id.id,
            'user_id': self.technician_user_id.id,
            'maintenance_team_id': self.maintenance_team_id.id,
            'duration': duration,
        })

    @api.model
    def create_custom_request(self):
        now_date = datetime.date.today()
        for equipment in self.search([('maintenance_plan', '=', 'fixed'), ('period', '>', 0)]):
            next_requests = self.env['maintenance.request'].search([('stage_id.done', '=', False),
                                                                    ('equipment_id', '=', equipment.id),
                                                                    ('repair_maintain', '=', 'maintain'),
                                                                    ('request_date', '=', equipment.next_action_date)])
            if not next_requests:
                if now_date == equipment.next_action_date:
                    equipment._create_maintain_request(equipment.next_action_date, equipment.maintenance_duration)
        for equipment in self.search([('maintenance_plan', '=', 'custom'), ('maintenance_line_ids', '!=', False)]):
            for date in equipment.maintenance_line_ids:
                next_requests = self.env['maintenance.request'].search([('stage_id.done', '=', False),
                                                                        ('equipment_id', '=', equipment.id),
                                                                        ('repair_maintain', '=', 'maintain'),
                                                                        ('request_date', '=',
                                                                         date.plan_date)])
                if not next_requests:
                    if now_date == date.plan_date:
                        equipment._create_maintain_request(date.plan_date, date.duration)

