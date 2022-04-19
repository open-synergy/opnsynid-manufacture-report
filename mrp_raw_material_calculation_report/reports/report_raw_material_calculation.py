# -*- coding: utf-8 -*-
# © 2015 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.lines = []
        self.temp_lines = []
        self.temp_dicts = {}
        self.localcontext.update(
            {
                "line": self._get_rm_lines,
            }
        )

    def set_context(self, objects, data, ids, report_type=None):
        obj_wizard = self.pool.get("mrp.wizard_raw_material_calculation")
        self.wizard = obj_wizard.browse(self.cr, self.uid, ids[0])
        return super(Parser, self).set_context(objects, data, ids, report_type)

    def _get_rm_lines(self):
        obj_bom = self.pool.get("mrp.bom")
        obj_uom = self.pool.get("product.uom")
        for detail in self.wizard.detail_ids:
            factor = obj_uom._compute_qty(
                self.cr,
                self.uid,
                detail.uom_id.id,
                detail.quantity,
                detail.bom_id.product_uom.id,
            )
            for bom_line in obj_bom._bom_explode(
                self.cr,
                self.uid,
                detail.bom_id,
                detail.product_id,
                factor / detail.bom_id.product_qty,
            )[0]:
                uom_id = bom_line["product_uom"]
                uom = obj_uom.browse(self.cr, self.uid, [uom_id])[0]
                bom_line.update({"uom": uom.name})
                self.temp_lines.append(bom_line)

        for temp_line in self.temp_lines:
            if "product_id" in temp_line:
                self.temp_dicts[temp_line["product_id"]] = temp_line
            else:
                self.temp_dicts[temp_line["product_id"]]["product_qty"] += temp_line[
                    "product_qty"
                ]

        for temp_dict in self.temp_dicts.values():
            self.lines.append(temp_dict)

        return self.lines
