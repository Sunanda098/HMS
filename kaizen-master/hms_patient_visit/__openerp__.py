{
    'name': 'Patient Visit',
    'version': '1.0.1',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Hospital Management System',
    'description': """
        Manage Patient Visits
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base', 'mail', 'account', 'hms'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_visit_view.xml',
        'views/patient_visit_menu.xml',
        'data/sequence.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
