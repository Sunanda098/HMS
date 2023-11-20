# -*- coding: utf-8 -*-

{
    'name': 'HMS Medical Procedure',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'description': """
        Thsi module adds Medical Procedure flow.
    """,
    "author": "Indimedi Solutions Pvt. Ltd.",
    'website': 'www.indimedi.com',
    'depends': ['base','mail','hms','hms_hospitalization'],
    'data': [
        'views/hms_medical_procedure_view.xml',
        'views/hms_medical_procedure_menu.xml',
        'data/hms_medical_procedure_data.xml',
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/medical_procedure_qweb.xml',
        'report/report_view.xml',
    ],
    'test': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
