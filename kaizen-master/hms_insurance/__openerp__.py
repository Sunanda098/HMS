# -*- coding: utf-8 -*-

{
    'name': 'Insurance Policy',
    'version': '1.0',
    'category': 'Hospital Management System',
    'sequence': 2,
    'summary': 'Insurance for Hospital Management System',
    'description': """
        Insurance for Hospital Management System
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base',
        'hms_document',
        'hms_hospitalization',
        'indimedi_hospitalization_shah',
        'account',
        'hms_vaccination',
        'hms_invoice',
        'stock',
    ],
    'data': [
        'security/security.xml',
        'views/claim_view.xml',
        'security/ir.model.access.csv',
        'reports/zero_error.xml',
        'reports/report_discharge.xml',
        'data/account_journal.xml',
        'views/claim_report_view.xml',
        'reports/claim_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
