 # -*- coding: utf-8 -*-

{
    'name': 'Hospital Care Plan Shah',
    'version': '1.0',
    'category': 'HMS',
    'summary': 'Hospital Care Plan for Shah Hospital',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['hms_hospitalization'],
    'data': [
             'security/ir.model.access.csv',
             'data/vulnerable_assessment.xml',
             'data/nursing_assessment_data.xml',
             'views/careplan_view.xml',
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
