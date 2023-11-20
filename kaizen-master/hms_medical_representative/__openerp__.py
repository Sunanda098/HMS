# -*- encoding: utf-8 -*-

{
    'name': 'Medical Representative',
    'category': 'App',
    'description': """
        This module Provides functionality to manage Medical Representative data and their visits 
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'version': '1.0.1',
    'sequence': 2,
    'depends': ["base",'hms'],
    'data' : [
        'views/mr_view.xml',
        'security/ir.model.access.csv',
        'data/mr_sequence.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
