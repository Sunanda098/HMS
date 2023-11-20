{
    'name': 'Unipath',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Unipath',
    'description': """
    In Unipath, Hospitalization Unipath,
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base','hms_investigation'],
    'data': [
        'security/ir.model.access.csv',
	    'views/unipath_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
