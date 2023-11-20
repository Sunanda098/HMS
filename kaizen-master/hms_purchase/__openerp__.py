# -*- encoding: utf-8 -*-

{
    'name': 'HMS Purchase MGMT',
    'version': "1.0",
    'sequence': 2,
    'author': "Indimedi Solutions Pvt. Ltd.",
    'summary': 'ICU Management System.',
    'description': """
        ICU Management System.
    """,
    'website': 'www.indimedi.com',
    'category': 'Hospital',
    'depends': ['sale',
                'purchase',
                'hms',
                'sale_stock',
                'account_voucher'
                ],
    'data': [
                "views/hms_purchase_view.xml",
             ],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
