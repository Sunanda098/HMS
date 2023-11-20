# -*- encoding: utf-8 -*-

{
    "name": "Indimedi Patient Barcode", 
    "version": "1.0", 
    'sequence': 2,
    "author": "Indimedi Solution", 
    "category": "Barcode", 
    "description": """
 Barcode For Patient
==================================

This module add barcode on patient.
""", 
    "website": "http://www.indimedi.in", 
    "depends": [
        "hms"
    ], 
    "data": [
        "data/ean_sequence.xml",
        "report/paper_format.xml",
        "report/report_view.xml",
        "views/patient_view.xml",
        "views/barcode_patient.xml",
        "wizard/patient_barcode_wizard.xml",
    ], 
    "installable": True, 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
