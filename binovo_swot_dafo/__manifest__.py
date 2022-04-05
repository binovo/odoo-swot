# -*- coding: utf-8 -*-
# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SWOT/DAFO",
    "summary": "Grouping the weaknesses, threats, strengths and opportunities",
    "version": "12.0.1.0.1",
    "author": "Binovo",
    "website": "http://www.binovo.es",
    "depends": [
        "mail",
    ],
    "data": [
        "security/swot_security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/swot_templates.xml",
        "views/swot_views.xml",
    ],
    "demo": [
        "data/swot_demo.xml"
    ],
    "installable": True,
    "auto_install": False,
}
