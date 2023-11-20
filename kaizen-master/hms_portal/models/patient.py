# -*- coding: utf-8 -*-
from openerp.tools.misc import ustr
from openerp import api, fields, models, _
from openerp.exceptions import UserError
import re

password = 'patient123'

class IndiPatient(models.Model):
    _inherit = 'hms.patient'

    @api.model
    def create(self, values):
        res = super(IndiPatient, self).create(values)
        group_id = self.env['ir.model.data'].get_object('base', 'group_portal')
        if not values.get('password'):
            res.user_id.write({'password':values.get('login')})
        group_id.write({'users': [(4, res.user_id.id)]})
        return res

    @api.multi
    def action_send_password(self):
        for patient in self:
            #send SMS
            temp_obj = self.env['mail.template']
            sms_obj = self.env['partner.sms.send']
            user_obj = self.env['res.users']
            template = False
            user = user_obj.browse(patient.user_id.id)
            user.write({'password':password})
            if not bool(template):
                template = self.env['ir.model.data'].get_object('auth_signup', 'reset_password_email')
            assert template._name == 'mail.template'

            
            if not user.email:
                raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
               
            if user.email and template:
                template.send_mail(user.id, force_send=True)

            if patient.mobile:
                message = _('Dear %s, Your Login is %s and Password is %s.Helpline: 07927552050.') % (patient.name,user.login,password)
                sms_id = sms_obj.create({
                    'mobile_to': patient.mobile,
                    'text': message,
                })
                sms_id.sms_send()

        return True

