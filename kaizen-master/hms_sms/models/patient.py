# -*- coding: utf-8 -*-

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models ,_
from openerp.exceptions import UserError

class IndiPatient(models.Model):
    _inherit = 'hms.patient'

    @api.model
    def create(self, values):
        #message remainder for patient for new registeration      
        print "===================create"
        res = super(IndiPatient, self).create(values)
        SmsObj = self.env['partner.sms.send']
        if values.get('mobile'):
            message = _('Dear %s, you have been registered as a patient with Shah Hospital. Your patient ID is %s. Helpline: 079 2755 2050.') % (values['name'], values['code'])
            sms_id = SmsObj.create({
                'mobile_to': values['mobile'],
                'text': message,
            })
            sms_id.sms_send()
        print "=================res",res
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
