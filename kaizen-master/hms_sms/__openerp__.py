# -*- coding: utf-8 -*-

{
    'name': 'HMS SMS',
    'version': '1.0',
    'category': 'Hospital Management System SMS',
    'sequence': 2,
    'summary': 'Contain all the message related content',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['sms_cellapps','hms','hms_vaccination'],
    'data': [
        'data/cron_sms_vaccination.xml',
        'data/appoint_remainder_data.xml',
        'views/doctor_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
