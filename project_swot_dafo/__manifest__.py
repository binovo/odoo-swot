# -*- coding: utf-8 -*-
# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Project SWOT/DAFO",
    "summary": "Relate projects to SWOT analyzes",
    "version": "12.0.1.0.0",
    "author": "Binovo",
    "category": "Project",
    "website": "http://www.binovo.es",
    "depends": [
        "project",
        "binovo_swot_dafo",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/swot_views.xml",
        "views/project_views.xml",
        "views/project_templates.xml",
        "wizard/add_swot_analysis_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
