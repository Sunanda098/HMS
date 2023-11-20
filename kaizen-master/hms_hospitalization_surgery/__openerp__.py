# -*- coding: utf-8 -*-

{
    'name': 'Hospitalization Surgery',
    'version': '1.0',
    'category': 'HMS',
    'summary': 'Surgery Pre-Operative notes and related surgery Record',
    'description': """
        This will add additional Button in hospitalization view called Surgery.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.in',
    'depends': ['hms_hospitalization'],
    'data': [
        'security/ir.model.access.csv',
        'views/surgery_view.xml',
        'data/sequence.xml',
        'data/ot_pre_checklist.xml',
        'data/pre_op_info_content.xml',
        'data/pre_op_investigation.xml',
        'data/fellow_checklist_data.xml',
        'data/anesthetist_checklist_data.xml',
        'data/op_surgeon_checklist_data.xml',
        'data/scrub_nurse_checklist_data.xml',
        'data/ot_charge_checklist_data.xml',
        'data/recovery_checklist_data.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: