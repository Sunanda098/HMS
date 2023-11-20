{
    'name': 'Outside Surgery ',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Outside Surgery',
    'description': """
    In Hospital, Hospitalization Outside Surgery,
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base','hms_insurance','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/outside_sequence.xml',
	    'views/outsider_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
