# -*- encoding: utf-8 -*-
{
    'name': 'Certificate Management',
    'category': 'HMS',
    'description': """
        This Module will Add functionality to provide certificate to patient and maintain history..
    """,
    'version': '1.0.1',
    'sequence': 2,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'depends': ["base","mail","hms"],
    'data' : [
        'security/certificate_security.xml',
        'data/certificate_sequence.xml',
        'views/certificate_management_view.xml',
        'report/certificate_content_report.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
