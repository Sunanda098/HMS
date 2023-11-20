# -*- coding: utf-8 -*-

{
    'name': 'Hms Products Manufacturers',
    'version': '1.0',
    'sequence': 2,
    'author': "OpenERP SA,Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'contributors': ['Acysos SL <info@acysos.com>'],
    'category': 'Purchase Management',
    'depends': ['product', 'hms'],
    'demo': [],
    'data': [
        'views/product_manufacturer_view.xml',
        'security/ir.model.access.csv'
    ],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
