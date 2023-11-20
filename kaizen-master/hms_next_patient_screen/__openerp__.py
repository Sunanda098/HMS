# -*- coding: utf-8 -*-
# 
{
    'name' : 'HMS Next patient Website page',
    'version' : '1.0.1',
    'author': 'Indimedi Solutions Pvt. Ltd.',
    'category': 'Website',
    'sequence': 2,
    'website' : 'http://indimedi.in/',
    'summary' : 'HMS Website',
    'description' : """
        This module provides page to show list of next patient who is going in consultation.
    """,
    'depends' : [
        'website','hms'
    ],
    'data' : [
         'views/next_patient_view.xml',
         'data/website_data.xml',
    ],
    'installable' : True,
    'application' : False,
}
