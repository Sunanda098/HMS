# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp import api, fields, models


class StockReturnPickingLine(models.TransientModel):
    _name = "stock.picking.barcode.line"
    _rec_name = 'product_id'
   
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Integer(string="Quantity", default=0, required=True)
    wizard_id = fields.Many2one('stock.picking.barcode', string="Wizard")
    lot_id = fields.Many2one('stock.production.lot',string='Serial Number', help="Used to choose the lot/serial number of the product returned")


class StockReturnPicking(models.TransientModel):
    _name = 'stock.picking.barcode'
    _description = 'Picking Barcode'
    
    @api.one
    def _starting_position(self,fields_name, arg):
        for report in self:
            self.report = (((report.rows-1)*5) + report.columns)-1

    columns = fields.Integer(string="Columns",default="1")
    rows = fields.Integer(string="Rows",default="1")
    starting_position = fields.Integer(compute=_starting_position,string="Position",readonly="True")
    product_barcode_line = fields.One2many('stock.picking.barcode.line', 'wizard_id',string='Barcode Wizard')

    @api.model
    def default_get(self,fields):
        result1 = []
        res = {}
        context = self._context or {}
        if context and context.get('active_ids', False):
            if len(context.get('active_ids')) > 1:
                raise osv.except_osv(_('Warning!'), _("You may only return one picking at a time!"))
        record_id = context and context.get('active_id', False) or False
        pick_obj = self.env['stock.picking']
        pick = pick_obj.browse(record_id)
        for move in pick.pack_operation_ids:
            result1.append({'product_id': move.product_id.id, 'lot_id': move.lot_id.id,'quantity': move.product_qty*move.product_id.uom_po_id.factor})
        if 'product_barcode_line' in fields:
            res.update({'product_barcode_line': result1})
        return res
    
    @api.multi
    def print_report(self):
        context = self._context or {}
        return self.pool['report'].get_action('indimedi_barcode_sale.report_picking_barcode')


class StockProductionReport(models.TransientModel):
    _name = 'stock.production.report'

    @api.one
    def _starting_position(self,fields_name, arg):
        for report in self:
            self.report = (((report.rows-1)*5) + report.columns)-1

    columns = fields.Integer(string="Columns",default="1")
    rows = fields.Integer(string="Rows",default="1")
    quantity = fields.Integer(string="Quantity",default="1")
    starting_position = fields.Integer(compute=_starting_position,string="Position",readonly="True")
    
    @api.one
    def print_report(self):
        context = self._context or {}
        datas = {'ids': context.get('active_ids', )}
        datas['form'] = self.read(ids)[0]
        return self.pool['report'].get_action('indimedi_barcode_sale.report_product_barcode', data=datas)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: