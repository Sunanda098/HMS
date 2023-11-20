# -*- encoding: utf-8 -*-

{
    "name": "Purchase Order with Barcode Reader", 
    "version": "1.0", 
    "author": "Indimedi Solution, Argil Consulting", 
    "category": "Purchase", 
    "description": """
Purchase Order with Barcode Reader
==================================

This module adds in Purchase Order Form View a new field to read Product EAN13
and adds such product as a Line in Purchase Order.
This module creates new Security Group, so only users in that Group will be able 
to use that field.
""", 
    "website": "http://www.indimedi.in, http://www.argil.mx", 
    "depends": [
        "purchase","stock","account","hms_batch_pricing"
    ], 
    "data": [
        "view/purchase_view.xml",
        "view/stock_view.xml", 
        "view/account_invoice_view.xml",
        "security/purchase_security.xml",
        "report/stock_production.xml",
        "report/stock_shipment.xml",
    ], 
    "test": [], 
    "js": [], 
    "css": [], 
    "qweb": [], 
    "installable": True, 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: