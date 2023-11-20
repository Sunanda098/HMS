# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management System',
    'version': '1.0.1',
    'category': 'HMS',
    'summary': 'Hospital Management System',
    'description': """
        Hospital Management System
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base', 'web', 'mail', 'web_timer_widget', 'account', 'product','auth_signup'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'data/hms_sequence.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        #'wizard/investigation_appointment_view.xml',
        'views/appointment_view.xml',
        'views/drug_view.xml',
        'views/diseases_view.xml',
        'views/referring_doctor_view.xml',
        'views/medicament_view.xml',
        'views/medication_dosage_view.xml',
        'views/template.xml',
        'report/paper_format.xml',
        'report/report_layout.xml',
        'report/report_layout_consent.xml',
        'report/report_layout_letterpad.xml',
        'report/patient_cardreport.xml',
        'report/template.xml',
        'views/menuitem.xml',
        'views/res_city_view.xml',
        'data/hms_data.xml',
        'data/res_country_state_data.xml',
        'data/res_city_data.xml',
        'report/medicament_groupreport.xml',
        'report/amo_agreement.xml',
        'data/disease_categories.xml',
        'data/diseases.xml',
    ],
    'demo': [

        'data/hms_doctor_demo.xml',
        'data/hms_patient_demo.xml',
        'data/hms_appointment_demo.xml',
        'data/hms_medicament_demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
