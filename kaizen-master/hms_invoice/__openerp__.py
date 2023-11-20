# -*- coding: utf-8 -*-
{
    "name" : "HMS Invoice",
    "version" : "1.1",
    'sequence': 2,
    "author" : "Indimedi Solutions Pvt. Ltd.",
    "description" : """ 
        This module add functionality to Print receipts.
        """,
    "website" : "www.indimedi.com",
    "depends" : ['account', 'account_voucher'],
    "category" : "Generic Modules/Others",
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
        "data/invoice_sequence.xml",
        "data/account_journal.xml",
        "data/account_data.xml",
        "report/report_account_payment_receipt.xml",
        "report/report_partial_payment_receipt.xml",
        "report/report_payment_receipt.xml",
        "report/report_account_invoice_receipt.xml",
        "report/report_view.xml",
        "views/account_invoice_view.xml",
        "views/account_payment_view.xml",
        "report/general_ledger.xml",
        "data/receipt_sequence.xml",
        "views/account_invoice_workflow.xml",
        "views/revenue_sharing_view.xml",
        "report/revenue_sharing_report_view.xml",
        "report/wizard_revenue_sharing_view.xml",
        "views/account_invoice_discount_view.xml",
        'report/report_hospital_inpatient_bill.xml',
        "security/ir.model.access.csv",
        
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
