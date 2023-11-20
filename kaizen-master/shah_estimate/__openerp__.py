{
    'name': 'Hospitalization Estimate Form',
    'version': '1.0',
    'sequence': 2,
    'category': 'HMS',
    'summary': 'Hospitalization form',
    'description': """
    Estimate Form,
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.com',
    'depends': ['base','hms', 'hms_hospitalization','hms_insurance'],
    'data': [
        'data/cost_estimation_data.xml',
        'security/ir.model.access.csv',
	    'views/estimation_view.xml',
        'report/report_hospital_estimate.xml',
        # 'report/report_cost_estimation.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
