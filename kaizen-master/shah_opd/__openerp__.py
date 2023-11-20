# -*- coding: utf-8 -*-

{
    'name': 'Indimedi HMS(Shah Hospital OPD)',
    'version': '1.0',
    'category': 'HMS',
    'summary': 'Hospital Management System',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base', 'hms', 'hms_prescription','web_timer_widget', 'hms_invoice','hms_investigation', 'hms_next_patient_screen'],
    'data': [
        'security/ir.model.access.csv',
#         'wizard/radiology_wizard.xml',
#         'wizard/pathology_wizard.xml',
#         'wizard/prescription_wizard.xml',
        'data/account_data.xml',
        'views/appointment_view.xml',
        'views/indimedi_prescription_view.xml',
        'views/template.xml',
        'report/prescription_report.xml',
        # 'report/prescription_groupreport.xml',
        'data/create_appointment.xml',
        
    ],
    'qweb' : ["static/src/xml/shah_appointment.xml",],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
