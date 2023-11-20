{
    'name': 'Hospitalization ',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Hospitalization',
    'description': """
    In Hospital, Hospitalization is include Inpatient Registration,Surgery,
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base','hms', 'hms_prescription'],
    'data': [
        'security/ir.model.access.csv',
        'security/hospitalization_security.xml',
        'data/consent_data.xml',
        'data/consent_data_update.xml',
        'wizard/transfer_accomodation_view.xml',
        'views/surgery_view.xml',
        'views/inpatient_view.xml',
        'views/bed_view.xml',
        'views/ward_view.xml',
        'views/hospital_building_view.xml',
        'views/hospital_or_view.xml',
        'views/cost_estimation_view.xml',
        'views/inpatient_prescription_view.xml',
        'views/sheet_custom.xml',
        'views/consent.xml',
        'report/report_hospital_discharge.xml',
        'report/report_attendance_pass.xml',
        'report/report_hospitalization_patient_card.xml',
        'report/report_cost_estimation.xml',
        'data/hospitalization_sequence.xml',
        'data/admission_check_list_data.xml',
        'data/pre_operaional_data.xml',
        'views/menuitem.xml',
        'data/ward_pre_checklist.xml',
        'views/ipd_report_view.xml',
        'report/ipd_report.xml',
        'report/report_operative_notes.xml',
        'report/team_admission_consent.xml',
        'report/intubation_report.xml',
        'report/ipd_stoma_consest.xml',
        'data/anesthesia.xml',
        'report/report_consent.xml',
        # 'data/nursing_admission_assessment.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
