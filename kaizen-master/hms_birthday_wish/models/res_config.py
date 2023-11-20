# -*- encoding: utf-8 -*-
from openerp import api, fields, models, tools


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'
        
    birthday_mail_template = fields.Many2one('mail.template', 'Birthday Wishes Template', required=True,
            help='This will set the default mail template for birthday wishes.')


    @api.multi
    def get_default_birthday_mail_template(self):
        user = self.env.user
        return {'birthday_mail_template': user.company_id.birthday_mail_template.id}

    @api.multi
    def set_birthday_mail_template(self):
        user = self.env.user
        user.company_id.write({'birthday_mail_template': self.birthday_mail_template.id})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
