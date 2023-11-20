# -*- coding: utf-8 -*-

{
    'name': 'Indimedi Shah Hospital',
    'version': '1.0',
    'category': 'HMS',
    'summary': 'Hospital APN and Ans Note',
    'description': """
        This will add additional Tabs in hospitalization view
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['hms_hospitalization', 'hms_operation_theatre'],
    'data': [
         'security/ir.model.access.csv',
         'views/indimedi_hospitalization_shah_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
