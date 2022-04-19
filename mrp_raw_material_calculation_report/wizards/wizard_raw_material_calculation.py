# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class WizardRawMaterialCalculation(models.TransientModel):
    _name = "mrp.wizard_raw_material_calculation"
    _description = "Print Raw Material Calculation"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        default="ods",
        selection=[("xls", "XLS"), ("ods", "ODS")],
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="mrp.wizard_raw_material_calculation_detail",
        inverse_name="wizard_id",
    )

    def button_print_report(self, cr, uid, ids, data, context=None):
        datas = {}
        output_format = ""

        if context is None:
            context = {}

        datas["form"] = self.read(cr, uid, ids)[0]

        if datas["form"]["output_format"] == "xls":
            output_format = "rreport_raw_material_calculation_xls"
        elif datas["form"]["output_format"] == "ods":
            output_format = "report_raw_material_calculation_ods"
        else:
            err = "Output Format cannot be empty"
            raise UserError(_("Warning"), _(err))

        return {
            "type": "ir.actions.report.xml",
            "report_name": output_format,
            "datas": datas,
        }


class WizardRawMaterialCalculationDetail(models.TransientModel):
    _name = "mrp.wizard_raw_material_calculation_detail"
    _description = "Print Raw Material Calculation Detail"

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_allowed_uom_ids(self):
        obj_uom = self.env["product.uom"]
        for document in self:
            result = []
            if document.product_id:
                uom_categ = document.product_id.uom_id.category_id
                criteria = [
                    ("category_id", "=", uom_categ.id),
                ]
                result = obj_uom.search(criteria).ids
            document.allowed_uom_ids = result

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_allowed_bom_ids(self):
        obj_bom = self.env["mrp.bom"]
        for document in self:
            result = []
            if document.product_id:
                product_tmpl = document.product_id.product_tmpl_id
                criteria = [
                    "|",
                    "&",
                    ("product_tmpl_id", "=", product_tmpl.id),
                    ("product_id", "=", False),
                    ("product_id", "=", document.product_id.id),
                ]
                result = obj_bom.search(criteria).ids
            document.allowed_bom_ids = result

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="mrp.wizard_raw_material_calculation",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    quantity = fields.Float(
        string="Qty.",
        required=True,
    )
    allowed_uom_ids = fields.Many2many(
        string="Allowed UoMs",
        comodel_name="product.uom",
        compute="_compute_allowed_uom_ids",
        store=False,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    allowed_bom_ids = fields.Many2many(
        string="Allowed BoMs",
        comodel_name="mrp.bom",
        compute="_compute_allowed_bom_ids",
        store=False,
    )
    bom_id = fields.Many2one(
        string="BoM",
        comodel_name="mrp.bom",
        required=True,
    )

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False

    @api.onchange(
        "product_id",
    )
    def onchange_bom_id(self):
        self.bom_id = False
