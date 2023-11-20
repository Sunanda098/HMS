# -*- coding: utf-8 -*-

{
    'name': 'HMS Consultation Report',
    'version': '1.0',
    'category': 'HMS',
    'sequence': 2,
    'summary': 'Consultation Report for Hospital Management System',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base','hms','report','shah_opd'],
    'data': [
       'security/ir.model.access.csv',
       'views/report_view.xml',
       'views/report.xml',
       'views/invoice.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
