# -*- coding: utf-8 -*-
{
    'name': 'HMS Vaccination',
    'version': '1.0.1',
    'category': 'HMS',
    'sequence': 2,
    'summary': 'Vaccination for Pediatrics',
    'description': """
        This Module will add a Page in Patient for managing Vaccine for Padetrics in HMS.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd',
    'website': 'www.indimedi.com',
    'depends': ['hms','sms_cellapps'],
    'data': [
         'security/ir.model.access.csv',
         'views/vaccination_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
