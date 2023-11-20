# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from openerp import api, fields, models, _
from openerp.exceptions import UserError
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class Appointment(models.Model):
    _inherit = 'hms.appointment'

    # Cron for Clear appointments after 20 min of booking if payment is not done.
    @api.model
    def clear_appointment_cron(self):
        #find appointment
        apps = self.search([('booked_online','=', True),('invoice_id.state','!=','paid')])
        for app in apps:
            create_time = datetime.strptime(app.create_date, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(minutes=20)
            if create_time <= datetime.now():
                #cancel appointment after 20 minute if not paid
                app.invoice_id.signal_workflow('invoice_cancel')
                app.write({'state': 'canceled'})
