# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013 Odoo All Rights Reserved.
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
	'name': "Web Form Edit Mode",
	'category': 'MRS',
    'sequence': 14,
    'summary': 'Inspection & Estimation',
	'description': """A module that force edit mode when loading a form view
	""",
	'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
	'depends': ['base'],
    'data': [],	
    'js': [
        'static/src/js/edit_form_view.js',
        'static/src/js/view_form.js',
        ],
    
}
