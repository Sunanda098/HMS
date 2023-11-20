# -*- coding: utf-8 -*-

{
    'name': 'HMS Lithotripsy',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Hospital Management System',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base', 'mail', 'account', 'report', 'hms_hospitalization'],
    'data': [
        'views/hms_lithotripsy_view.xml',
        #'views/hms_report.xml',
        'data/sequence.xml',
        #'security/ir.model.access.csv'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
