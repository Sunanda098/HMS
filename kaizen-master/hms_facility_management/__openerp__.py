# -*- encoding: utf-8 -*-
{
    'name': 'Facility Management',
    'category': 'App',
    'description': """
        This module allows you to manage your facility related stuff.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'version': '1.0.1',
    'sequence': 2,
    'depends': ["base", "mail"],
    'data' : [
        'data/facility_sequence.xml',
        'views/facility_management_view.xml',
        'data/cron_create_task.xml',
        'security/facility_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
