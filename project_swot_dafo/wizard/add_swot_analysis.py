# -*- coding: utf-8 -*-
# © 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.addons.binovo_swot_dafo.models.swot import ANALYSIS_TYPES


class PaymentDebitOrder(models.TransientModel):
    _name = 'add.swot.analysis.wizard'

    analysis_type = fields.Selection(selection=ANALYSIS_TYPES, string='Type', required=True)

    def add_analysys_type(self):
        self.ensure_one()
        views = [(self.env.ref('binovo_swot_dafo.swot_analysis_view_form').id, 'form')]
        context = dict(self._context or {})
        context.update({'default_type': self.analysis_type})
        return {
            'name': _('Swot analysis'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'swot.group.analysis',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'views': views,
            'auto_refresh': 1,
            'context': context,
        }
