# -*- coding: utf-8 -*-

{
    'name': 'Paediatric',
    'version': '1.0',
    'category': 'Hospital Management System',
    'sequence': 2,
    'summary': 'Paediatric appointment and patient management',
    'description': """
        Paediatric appointment and patient management
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.in',
    'depends': ['base', 'hms', 'hms_prescription', 'shah_opd', 'hms_hospitalization', 'hms_document'],
    'data': [
        'security/ir.model.access.csv',
        'security/hms_security.xml',
        'views/paediatric_view.xml',
        'views/paediatric_menu.xml',
        'data/paediatric_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
