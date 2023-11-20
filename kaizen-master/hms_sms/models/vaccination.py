# -*- coding: utf-8 -*-
from openerp import api, fields, models ,_
from datetime import date, datetime, timedelta as td

class Vaccination(models.Model):
    _inherit = 'vaccination.vaccination'

    #sms for vaccination remainder on due date for patient and doctor
    @api.model
    def create_sms_vaccination(self):
        SmsObj = self.env['partner.sms.send']
        vaccinations = self.search([('date_check_due','>', (datetime.now()+td(days=1)).strftime('%Y-%m-%d')),('date_check_due','<', (datetime.now()+td(days=3)).strftime('%Y-%m-%d'))])
        for vac in vaccinations:
            if vac.patient_id.mobile:
                message = ('%s, Please visit Dr.%s,Shah Hospital for %s Vaccination on %s.HelpLine: 079 2755 20500.') % (vac.patient_id.name,vac.patient_id.primary_doctor.name,vac.product_id.name,vac.date_check_due)
                sms_id = SmsObj.create({
                   'text': message,
                   'mobile_to': vac.patient_id.mobile,
                })
                sms_id.sms_send()
            if vac.patient_id.primary_doctor.sms_vaccination:
                message = ('Dr.%s, you have an appointment with %s for %s Vaccination on %s.HelpLine: 079 2755 20500.') % (vac.patient_id.primary_doctor.name,vac.patient_id.name,vac.product_id.name,vac.date_check_due)
                sms_id = SmsObj.create({
                   'text': message,
                   'mobile_to': vac.patient_id.primary_doctor.mobile,
                })
                sms_id.sms_send()     

