# -*- coding: utf-8 -*-
{
    'name': 'Indian Localization for HMS',
    'version': '1.0',
    'category': 'Indian Localization',
    'summary':'Reports based on IRDA rules, Added support of city, data of List of States and Cities in India',
    'description': """
        This module will add city in address as per indian address requirement. Adds data of state and city. Added ihospital bill reports based on irda Rules.
    """,
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'website': 'www.indimedi.in',
    'depends': ['hms'],
    'data': [
       'data/irda_data.xml',
       'security/ir.model.access.csv',
       'report/report_view.xml',
       'report/report_standard_bill.xml',
       'report/report_standard_discharge.xml',
       'views/irda_view.xml',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
