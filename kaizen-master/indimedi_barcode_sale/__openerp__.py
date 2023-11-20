# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to Odoo, Open Source Management Solution
#
#    Copyright (c) 2015 Argil Consulting - http://www.argil.mx
#    Copyright (c) 2015 Indimedi Solution - http://www.indimedi.in
############################################################################
#    Coded by: Israel Cruz (israel.cruz@argil.mx)
############################################################################
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
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
{
    "name": "Indimedi Barcode", 
    "version": "1.0", 
    "author": "Indimedi Solution", 
    "category": "Barcode", 
    "description": """
 Barcode Reader
==================================

This module add barcode report in Product.
""", 
    "website": "http://www.indimedi.in", 
    "depends": [
        "sale","stock"
    ], 
    "data": [
        'security/ir.model.access.csv',
        "report/paper_format.xml",
        "report/stock_report.xml",
        "views/barcode_product.xml",
        "views/sale_view.xml",
        "wizard/stock_wizard.xml",
    ], 
    "installable": True, 
}
