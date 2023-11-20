# -*- coding: utf-8 -*-

{
    'name': 'HMS - ICU MGMT',
    'version': '1.0.1',
    'category': 'HMS',
    'summary': 'ICU Management System.',
    'description': """
        ICU Management System.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.in',
    'depends': ['hms', 'hms_hospitalization', 'hms_treatment'],
    'data': [
       'security/ir.model.access.csv',
       'views/hms_icu.xml',
       'views/hms_icu_css.xml',
       'reports/icu_chart_report.xml',
       'reports/investigations_report.xml',
       'reports/rbs_report.xml',
       'data/sequence.xml',
       'data/icu_schedluar.xml',
       'data/diet_value.xml',
       'reports/doctor_invoice.xml',
       'reports/patient_invoice.xml',
       'views/hms_icu_hospitalization.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
