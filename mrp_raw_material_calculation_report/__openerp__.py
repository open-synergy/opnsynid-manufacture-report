# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Raw Materia Calculation Report",
    "version": "8.0.1.0.1",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "depends": [
        "mrp",
        "report_aeroo",
    ],
    "installable": True,
    "license": "AGPL-3",
    "data": [
        "wizards/wizard_raw_material_calculation.xml",
        "reports/report_raw_material_calculation_ods.xml",
        "reports/report_raw_material_calculation_xls.xml",
    ],
}
