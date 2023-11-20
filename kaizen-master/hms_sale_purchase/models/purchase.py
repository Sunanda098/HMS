# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    po_uom_rate = fields.Float(string="Purchase UOM Rate",
        help="Set Rate of purchase UOM and it will set Unit price automatically.")
    so_uom_rate = fields.Float(string="Sale UOM Rate",
        help="Set Rate of Sale for purchasse UOM and it will set sale Unit price automatically.")

    @api.onchange('po_uom_rate','uom_po_id', 'po_uom_rate')
    def _onchange_po_uom_rate(self):
        if self.po_uom_rate and self.uom_po_id:
            self.standard_price = self.po_uom_rate / self.uom_po_id.factor_inv

        if self.so_uom_rate and self.uom_po_id:
            self.list_price = self.so_uom_rate / self.uom_po_id.factor_inv

        return

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: