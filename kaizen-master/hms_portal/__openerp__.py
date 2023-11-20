# -*- coding: utf-8 -*-
# 
{
    'name' : 'HMS Portal',
    'version' : '1.0.1',
    'author' : 'Indimedi Solutions',
    'category': 'Website',
    'sequence': 2,
    'website' : 'https://indimedi.in/',
    'summary' : 'HMS Portal',
    'description' : """
HMS Website Portal 
Sign up create patient and Book an appointment online.
""",
    'depends' : [
        'website','hms','portal','sms_cellapps','hms_hospitalization','hms_document','shah_opd','website_payment','l10n_in','account_cancel'
    ],
    'data' : [
         'data/weekly_slot_cron_view.xml',
         'data/template_data.xml',
         'views/schedual_views.xml',
         'views/hms_portal_view.xml',
         'views/template.xml',
         'views/signup.xml',
         'security/ir.model.access.csv',
         'wizard/appointment_schedular_wizard.xml',
    ],

    'installable' : True,
    'application' : False,
}
