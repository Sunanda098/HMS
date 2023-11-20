# -*- encoding: utf-8 -*-
{
    'name': 'Indimedi Document',
    'version': '1',
    'category': 'HMS',
    'description': """Add Multiple documents to records
    """,
    'author': '',
    'license': 'AGPL-3',
    'website': 'http://www.indimedi.in',
    'depends': [
        'base','hms'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/document_view.xml'
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
