# -*- encoding: utf-8 -*-

{
    'name': 'HMS Sale and Purchase',
    'version': "1.0",
    'sequence': 2,
    'author': "Indimedi Solutions Pvt. Ltd.",
    'website': 'www.indimedi.com',
    'category': 'Hospital',
    'depends': ['sale',
                'purchase',
                'hms',
                'sale_stock',
                'account_voucher'
                ],
    'data': [
             "views/sale_view.xml",
             "views/purchase_view.xml",
             ],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
