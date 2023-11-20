# -*- coding: utf-8 -*-

{
    'name': 'Indimedi Investigation',
    'version': '1.0.1',
    'category': 'Hospital Management System',
    'sequence': 2,
    'summary': 'Base Module for Hospital Management System',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base', 'web', 'hms', 'hms_hospitalization', 'hms_document', 'hms_image_zoom'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/account_data.xml',
        'data/sequence.xml',
        'views/investigation_view.xml',
    ],
    'demo': [
        'data/hms_investigation_demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
