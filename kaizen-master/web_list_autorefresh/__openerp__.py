# -*- coding: utf-8 -*-

{
    'name': 'Auto Refresh List Views',
    'version': '0.1',
    'category': 'web',
    'description': """This module use the Auto Refresh List view""",
    'author': 'Indimedi Solution',
    'website': 'www.indimedi.in',
    'depends': ['base', 'web'],
    'data': ['views/assets.xml'],
    "qweb": [
        'static/src/xml/list_view.xml',
    ],
    'active': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
