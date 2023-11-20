# -*- coding: utf-8 -*-

{
    'name' : 'HMS Treatment',
    'version' : '0.1',
    'author' : 'Indimedi Solutions',
    'category': 'Website',
    'sequence': 2,
    'website' : 'https://indimedi.in/',
    'summary' : 'HMS Treatment',
    'description' : """
        HMS Treatment
    """,
    'depends' : [
        'shah_opd','hms_hospitalization','hms_insurance'
    ],
    'data' : [
         'security/ir.model.access.csv',
         'report/treatmentsheet_report.xml',
         'report/treatment_reports_view.xml',
         'report/report_line_treatment.xml',
         'views/hms_treatment_view.xml',
    ],

    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
