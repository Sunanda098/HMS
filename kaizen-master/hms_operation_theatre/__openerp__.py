# -*- coding: utf-8 -*-

{
    'name': 'HMS Operation Theatre',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Hospital Management System',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base', 'mail', 'hms_hospitalization'],
    'data': [
        'security/ir.model.access.csv',
        'data/ot_sequence.xml',
        'views/ot_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
