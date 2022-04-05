# -*- coding: utf-8 -*-
# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, _

class Project(models.Model):
    _inherit = 'project.project'

    swot_analysis_ids = fields.One2many('swot.group.analysis', 'project_id', 'Analysis', readonly=True)
    weaknesses_ids = fields.One2many('swot.group.analysis', 'project_id', domain=[('type', '=', 'weaknesses')])
    threats_ids = fields.One2many('swot.group.analysis', 'project_id', domain=[('type', '=', 'threats')])
    strengths_ids = fields.One2many('swot.group.analysis', 'project_id', domain=[('type', '=', 'strengths')])
    opportunities_ids = fields.One2many('swot.group.analysis', 'project_id', domain=[('type', '=', 'opportunities')])

    def add_analysis(self):
        self.ensure_one()
        views = [(self.env.ref('project_swot_dafo.view_add_swot_analysis_wizard_form').id, 'form')]
        context = dict(self._context or {})
        context.update({'default_project_id': self.id})
        res = self.env['swot.group.analysis'].search([('project_id', '=', self.id)])
        if res and 0 < len(res):
            context.update({'default_group_id': res[0].group_id.id})
        return {
            'name': _('Add swot analysis'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'add.swot.analysis.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'views': views,
            'auto_refresh': 1,
            'context': context,
        }
