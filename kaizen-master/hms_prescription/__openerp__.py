
{
    'name': 'Prescription',
    'version': '1.0',
    'category': 'Hospital Management',
    'sequence': 2,
    'summary': 'Base Module for Hospital Management',
    'description': """
        This module adds Prescription functionality
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['hms', 'sale', 'stock', 'product', 'purchase','board'],
    'data': [
        'views/hms_family_view.xml',
        'views/hms_prescription_order_view.xml',
        'views/hms_indoor.xml',
        'views/hms_prescription_line_view.xml',
        'views/hms_patient_medication_view.xml',
        'views/menu_view.xml', 
        'views/hms_patient_view.xml',
        'report/report_hms_prescription.xml',
        'report/grn_report.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'data/prescription_order_data.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
