# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
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


{
    'name': 'Indimedi KRA',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Indimedi KRA',
    'description':"""Indimedi KRA""",
    'author': 'Indimedi',
    'depends': ['hr', 'hr_contract', 'hr_holidays', 'indimedi_survey'],
    'website': '',
    'data': [
              #'report/indimedi_kra_report.xml', 
              'views/indimedi_kra_view.xml',
              'wizard/fill_kra_view.xml', 
              'security/indimedi_kra_security.xml',
              'security/ir.model.access.csv',
              'data/indimedi_kra_data.xml', 
              'data/company_data.xml', 
              'report/views/report.xml',
              'report/views/appointment_letter.xml',
              'report/views/report_rating.xml',
              'report/views/full_and_final_settlement_letter.xml',
              'report/views/appreciation_letter.xml',
              'report/views/confirmation_letter.xml',
              'report/views/probation_extension.xml',
              'report/views/experience_letter_format.xml',
              'report/views/consent_letter.xml',
              'report/views/offer_letter.xml',
              'report/views/nursing_credential_letter.xml',
              'views/hr_employee_view.xml',
              #'data/employee_data.xml'
              ],
    'demo_xml': [],
    'css': [ '*.css' ],
    'js': ['*.js' ],
    'installable': True,
    'active': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
