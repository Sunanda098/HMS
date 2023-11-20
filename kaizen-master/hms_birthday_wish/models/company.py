# -*- encoding: utf-8 -*-

from openerp import api, fields, models, _
from datetime import datetime, timedelta, time

class ResCompany(models.Model):
    _inherit = 'res.company'

    birthday_mail_template = fields.Many2one('mail.template', 'Birthday Wishes Template',
            help="This will set the default mail template for birthday wishes.")
    invoiced = fields.Boolean('Invoiced')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
