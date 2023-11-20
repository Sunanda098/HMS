# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Indimedi Survey',
    'version': '1.0',
    'category': 'hr',
    'author': 'Indimedi',
    'description': """
    """,
    'website': 'www.indimedi.in',
    'depends': ['base', 'hr', 'survey', 'hr_evaluation', 'mail', 'project','hr_timesheet_sheet'],
    'data': [
        'views/indimedi_survey_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
