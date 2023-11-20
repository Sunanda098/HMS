# -*- encoding: utf-8 -*-

{
    'name': 'HMS X-Ray Report',
    'category': 'App',
    'description': """
        This Module will add button in patient to print X-Ray report,menu after investigation.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'version': '1.0',
    'sequence': 2,
    'depends': ["base","mail","hms","hms_investigation"],
    'data' : [
        'security/ir.model.access.csv',
        'data/xray_sequence.xml',
        'views/xray_management_view.xml',
        'report/xray_content_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
