{
    'name': 'Store Management',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Store Manager',
    'description': """
    Consent Form,
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['stock','hr','base'],
    'data': [
            'views/request_view.xml',
            'views/product_request_mail.xml',
            'views/product_request_approved_mail.xml',
            'security/ir.model.access.csv',
            'security/hms_security.xml',
            
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
