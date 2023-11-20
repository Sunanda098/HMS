# -*- coding: utf-8 -*-

from openerp.osv import osv, orm, fields
from openerp import api, fields, models, _
from datetime import datetime, timedelta, time

class Doctor(models.Model):
    _inherit = 'hms.physician'

    sms_remainder_appointment = fields.Boolean('Sms Appointment', default=True)
    sms_vaccination = fields.Boolean('Sms Vaccination', default=True)

class Appointment(models.Model):
    _inherit = 'hms.appointment'
    #sms remainder for patient appointment to patient
    @api.model
    def send_sms_remainder(self):
        sms_obj = self.env['partner.sms.send']
        appointment_ids = self.search([('date','>=', (datetime.now()+timedelta(hours=24)).strftime('%Y-%m-%d 00:00:00')),('date','<=', (datetime.now()+timedelta(hours=48)).strftime('%Y-%m-%d 00:00:00')),('state','=','draft')])
        follow_up_ids = self.search([('date','>=', (datetime.now()+timedelta(hours=24)).strftime('%Y-%m-%d 00:00:00')),('date','<=', (datetime.now()+timedelta(hours=48)).strftime('%Y-%m-%d 00:00:00')),('consultation_type','=','followup'),('state','=','draft')])
        for appoint in appointment_ids:
            date_string = appoint.date
            opp_date = datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
            opp_time = (datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S")+timedelta(hours=5,minutes=30)).strftime("%H:%M")
            if appoint.patient_id.mobile:
                message = _('%s, Your appointment has been scheduled with Dr.%s,Shah Hospital on %s at %s.HelpLine: 079 2755 2050.') % (appoint.patient_id.name,appoint.patient_id.primary_doctor.name,opp_date,opp_time)
                sms_id = sms_obj.create({
                   'text': message,
                   'mobile_to': appoint.patient_id.mobile,
                })
                sms_id.sms_send()
            if appoint.patient_id.primary_doctor.sms_remainder_appointment:
                message = _('Dear Dr.%s, you have an appointment with %s on %s at %s.HelpLine: 079 2755 2050.') % (appoint.patient_id.primary_doctor.name,appoint.patient_id.name,opp_date,opp_time)
                sms_id = sms_obj.create({
                   'text': message,
                   'mobile_to': appoint.patient_id.primary_doctor.mobile,
                })
                sms_id.sms_send()
        for follow in follow_up_ids:
            date_string = follow.date
            opp_date = datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
            opp_time = (datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S")+timedelta(hours=5,minutes=30)).strftime("%H:%M")
            if follow.patient_id.mobile:
                message = _('%s,Please visit Dr.%s,Shah Hospital for %s on %s at %s.Helpline: 079 2755 2050.') % (follow.patient_id.name,follow.patient_id.primary_doctor.name,follow.purpose_id.name,opp_date,opp_time)
                sms_id = sms_obj.create({
                       'text': message,
                       'mobile_to': follow.patient_id.mobile,
                       })
                sms_id.sms_send()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
