# -*- coding: utf-8 -*-
{
    'name': 'Gynec Management System',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Gynec Management System',
    'description': """
        Module to manage Gynec procedures.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['hms','hms_medical_procedure'],
    'data': [
        'security/ir.model.access.csv',
        'views/hms_gynec_view.xml',
        'views/hms_appointment_view.xml',
        'views/hms_sonography_view.xml',
        'views/hms_delivery_view.xml',
        'report/report_medical_advice.xml',
        'report/consultation_report.xml',
        'report/report_sono_follical.xml',
        'report/report_sono_pelvis.xml',
        'report/report_sono_obstetric.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
