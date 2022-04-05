# -*- coding: utf-8 -*-
# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.modules import get_module_resource

import base64
import json

ANALYSIS_TYPES = [
    ('weaknesses', 'Weaknesses'),
    ('threats', 'Threats'),
    ('strengths', 'Strengths'),
    ('opportunities', 'Opportunities')
]


class SwotGroup(models.Model):
    _name = 'swot.group'
    _description = 'SWOT group'
    _inherit = ['mail.thread']

    def _get_default_manager(self):
        return [(6, 0, [self.env.uid])]

    def _compute_analysis_count(self):
        for group in self:
            group.analysis_count = len(group.analysis_ids)

    def _compute_totals_list(self):
        for res in self:
            group_obj = self.env['swot.group.analysis'].read_group([
                ('group_id', '=', res.id)], fields=['type'],
                groupby=['type'], orderby='type')
            totals = []
            for type in group_obj:
                totals.append({'type': type['type'], 'count': type['type_count']})
            res.totals_list = json.dumps(totals)

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string='Color Index')
    manager_ids = fields.Many2many(comodel_name='res.users', string='Managers',
                                   domain=lambda self: [("groups_id", "in", [self.env.ref("binovo_swot_dafo.group_swot_manager").id, self.env.ref("binovo_swot_dafo.group_swot_user").id])],
                                   default=lambda self: self._get_default_manager())
    analysis_ids = fields.One2many('swot.group.analysis', 'group_id', string='Analysis')
    totals_list = fields.Text(compute='_compute_totals_list')
    analysis_count = fields.Integer(compute='_compute_analysis_count', string='Analysis Count')

    @api.multi
    def unlink(self):
        for swot_group in self:
            if swot_group.analysis_ids:
                raise UserError(_('You cannot delete a SWOT group containing analysis. You can either delete all the group\'s analysis and then delete the SWOT group.'))
        res = super().unlink()
        return res


class SwotAnalisysSubtype(models.Model):
    _name = 'swot.analysis.subtype'
    _description = 'Analysis subtypes'

    name = fields.Char(string="Name", required=True, translate=True)


class SwotAnalysisStage(models.Model):
    _name = 'swot.analysis.stage'
    _description = 'Analysis Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(default=1)


class SwotAnalysisTags(models.Model):
    _name = "swot.analysis.tags"
    _description = "Tags of analysis"

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index', default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class SwotGroupAnalisys(models.Model):
    _name = 'swot.group.analysis'
    _description = 'Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['swot.analysis.stage'].search([], order="sequence", limit=1).id

    @api.depends('type')
    def _compute_type_image(self):
        for res in self:
            img_path = get_module_resource(
                'binovo_swot_dafo', 'static/src/img',
                'ico_' + str(res.type) + '.png'
            )
            if img_path:
                with open(img_path, 'rb') as f:
                    res.type_image = base64.b64encode(f.read())

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    name = fields.Char("Title", required=True)
    active = fields.Boolean("Active", default=True)
    description = fields.Html(string="Description")
    agreements = fields.Html(string="Agreements")
    type = fields.Selection(selection=ANALYSIS_TYPES, string='Type', required=True)
    type_image = fields.Binary(compute="_compute_type_image")
    group_id = fields.Many2one('swot.group', string='SWOT group',
                               default=lambda self: self.env.context.get('default_group_id'),
                               index=True, required=True, change_default=True)
    priority = fields.Selection(
        selection=[
            ('0', 'Very Low'),
            ('1', 'Low'),
            ('2', 'Normal'),
            ('3', 'High')],
        index=True)
    manager_ids = fields.Many2many(comodel_name='res.users',
                                   string='Managers',
                                   domain=lambda self: [("groups_id", "in", [self.env.ref("binovo_swot_dafo.group_swot_manager").id, self.env.ref("binovo_swot_dafo.group_swot_user").id])])
    date = fields.Date('Date', required=True, default=fields.Date.context_today, track_visibility='onchange')
    date_deadline = fields.Date(string='Deadline', index=True, copy=False, track_visibility='onchange')
    stage_id = fields.Many2one('swot.analysis.stage', string='Stage',
                               track_visibility='onchange', index=True,
                               default=_get_default_stage_id,
                               group_expand='_read_group_stage_ids',
                               copy=False)
    subtype_id = fields.Many2one('swot.analysis.subtype', string='Subtype')
    color = fields.Integer(string='Color Index')
    tag_ids = fields.Many2many('swot.analysis.tags', string='Tags')
