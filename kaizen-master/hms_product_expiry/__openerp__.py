# -*- encoding: utf-8 -*-

{
    "name": "Products Expiry Date - Extension",
    "version": "1.0",
    'sequence': 2,
    "depends": [
        "stock",
        "product_expiry",
    ],
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "category": "Tools",
    "website": "http://www.indimedi.com",
    "summary": "",
    "data": [
        "views/production_lot_ext_view.xml",
        "views/stock_quant_view.xml",
        #'security/ir.model.access.csv' 
      #  "wizard/stock_transfer_details_view.xml",
    ],
    "installable": True,
}
