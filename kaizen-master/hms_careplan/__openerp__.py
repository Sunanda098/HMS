 # -*- coding: utf-8 -*-

{
    'name': 'Hospital Care Plan',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Hospital Care Plan',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base', 'hms', 'hms_hospitalization', 'product'],
    'data': [
             'security/ir.model.access.csv',
             'views/careplan_view.xml',
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
