# -*- encoding: utf-8 -*-
{
    "name": "Birthday Wish/Notifications",
    "version": "1.0",
    'sequence': 2,
    "author": "Indimedi Solutions Pvt. Ltd.",
    "category": "Other",
    "website": "www.indimedi.com",
    "description": """In any business customer relations are most important and for any one their bithday is alwasy special so wish your clients using this module and improve your relations. Send Birthday Wishes via mail, get birthday Notifications and wish your customers.""",
    "summary": "Send Birthday Wishes via mail, get birthday Notifications and wish your customers",
    "license": "AGPL-3",
    "depends": ['hms', 'mail', 'sms_cellapps'],
    'data':[
        'views/res_config_view.xml',
        'data/template_data.xml',
        'data/wish_cronjob.xml',
    ],
    "installable": True,
    "auto_install": False,
    "active": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
