# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from openerp import api, fields, models, _
from openerp.exceptions import UserError


class AppointmentSchedularWizard(models.TransientModel):
    _name = 'appointment.schedular.wizard'

    @api.multi
    def _check_dates(self):
        for wizard in self:
            if wizard.start_date > wizard.end_date:
                return False
        return True
        
    start_date = fields.Date('Start Date', required=True, default=fields.Datetime.now)
    end_date = fields.Date('End Date',required=True) 
    
    _constraints = [(_check_dates, "Schedular 'Start Date' must be before 'End Date'.", ['start_date', 'end_date'])]
    
    @api.multi
    def appointment_slot_create_wizard(self):
        slot_obj = self.env['appointment.schedual.slot']
        
        # create slot
        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        
        while (start_date != end_date + timedelta(days=1)):
            cron = self.env['ir.model.data'].get_object('hms_portal', 'ir_cron_create_slot')
            slot_found = slot_obj.search([('slot_date','=',start_date.strftime("%m/%d/%Y"))])
            if slot_found:
                raise UserError(_("Appointment Slot exist for date %s." % start_date.strftime("%m/%d/%Y")))
            slot_obj.create_appointment_slot(start_date)
            start_date = start_date  + timedelta(days=1)
        end_schedular =(end_date - timedelta(days=7)).strftime("%m/%d/%Y")
        cron.write({'nextcall':end_schedular})
           
        
        
        
