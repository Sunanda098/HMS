# -*- coding: utf-8 -*-

{
    'name': 'HMS Bone Bank',
    'version': '1.0.2',
    'category': 'HMS',
    'sequence': 2,
    'summary': 'Hospital Bone Bank Management System',
    'description': """
        This Module will install Bone Bank Module, which will help to register user, and managed bone 
        in the Bone Bank.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['hms'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/bone_bank_view.xml',
        'data/bone_bank_sequence.xml',
        'report/survey_paper_format.xml',
        'report/survey_form.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
