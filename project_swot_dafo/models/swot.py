# -*- coding: utf-8 -*-
# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SwotGroupAnalisys(models.Model):
    _inherit = 'swot.group.analysis'

    project_id = fields.Many2one('project.project', string='Project')
