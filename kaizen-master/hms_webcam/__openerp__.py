# -*- encoding: utf-8 -*-

{
    'name': 'Patient picture with webcam',
    'version': '1.0',
    'sequence': 2,
    'category': 'Hospital',
    'description': """Capture Patient pictures with an attached webcam.""",
    'author': "Indimedi Solutions Pvt. Ltd.",
    'website': 'www.indimedi.com',
    'license': 'AGPL-3',
    'depends': ['hms'],
    'data': [
        'views/patient_webcam_view.xml',
    ],
    'qweb' : [
        "static/src/xml/patient_webcam.xml",
    ],
    'installable': True,
    'active': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
