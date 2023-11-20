# -*- coding: utf-8 -*-
from openerp.tools.misc import ustr
from openerp import api, fields, models, _
from ast import literal_eval
from openerp.http import request

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    @api.model
    def _signup_create_user(self, values):
        mobile = values.pop('mobile','')
        res = super(ResUsers, self)._signup_create_user(values)
        patient = self.env['hms.patient'].with_context(online=True).create({
            'user_id': res,
            'tz':'Asia/Calcutta',
            'mobile': mobile,
            'first_name':values.get('name')
        })
        return res
        
class ResPartnerHMSPortal(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def signup_retrieve_info(self, token):
        res = super(ResPartnerHMSPortal, self).signup_retrieve_info(token)
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        res.update({'mobile':partner.mobile})
        return res

