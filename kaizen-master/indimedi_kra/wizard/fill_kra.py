# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 Indimedi - http://www.indimedi.com
#    All Rights Reserved.
#    Indimedi (info@indimedi.com)
#
#    Coded by: Turkesh Patel (turkesh@indimedi.com)
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

from openerp.osv import osv, orm, fields


class kra_wizard(orm.TransientModel):
    _name = "kra.wizard"
    _description = "KRA Wizard"

    _columns = {
        'month_from':fields.selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'october'), (11, 'November'), (12, 'December') ], "Month from"),
        'month_to': fields.selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'october'), (11, 'November'), (12, 'December') ], "Month to"),
        'employee_id': fields.many2one('hr.employee', 'Employee'),
        'year': fields.many2one('indimedi.year', 'Year'),
    }

    _defaults = {
       'month_from': 1,
       'month_to':2,
       'employee_id':1,
       }


    def print_kra_report(self, cr, uid, ids, context=None):
        return  {'type': 'ir.actions.report.xml',
                 'report_name': 'kra.wizard.report',
                 'datas':  {'model': 'kra.wizard', 'ids': ids},
                 'nodestroy': True}

    def print_value_rating(self, cr, uid, ids, context=None):
        return  {'type': 'ir.actions.report.xml',
                 'report_name': 'value.rating.wizard',
                 'datas':  {'model': 'kra.wizard', 'ids': ids},
                 'nodestroy': True}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
