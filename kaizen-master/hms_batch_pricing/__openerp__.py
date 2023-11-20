# -*- coding: utf-8 -*-

{
    'name': 'Batch Wise Pricing',
    'version': '1.0',
    'category': 'Hospital Management System',
    'sequence': 2,
    'summary': 'Module for Batch Wise Pricing for HMS',
    'description': """

    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['stock', 'sale', 'hms_sale_purchase'],
    'data': [
        #'security/ir.model.access.csv'
        'views/batch_wise_pricing_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
