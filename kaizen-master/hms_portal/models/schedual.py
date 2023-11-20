# -*- coding: utf-8 -*-

import datetime
from datetime import timedelta
from openerp import api, fields, models, _
from openerp.tools.float_utils import float_compare
from openerp.exceptions import UserError
import pytz
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class AppointmentSchedual(models.Model):
    _name = "appointment.schedual"
    _description = "Appointment Schedual"

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get())
    schedual_lines = fields.One2many(
        'appointment.schedual.lines', 'schedual_id', string='Schedual Lines',
        copy=True)

class AppointmentSchedualLines(models.Model):
    _name = "appointment.schedual.lines"
    _description = "Appointment Schedual Lines"
    _order = 'dayofweek, hour_from'

    name = fields.Char(required=True)
    dayofweek = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
        ], 'Day of Week', required=True, index=True, default='0')
    hour_from = fields.Float(string='Work from', required=True, index=True, help="Start and End time of working.")
    hour_to = fields.Float(string='Work to', required=True)
    schedual_id = fields.Many2one("appointment.schedual", string="Appointment Schedual", required=True)


class AppointmentSchedualSlot(models.Model):
    _name = "appointment.schedual.slot"
    _description = "Appointment Schedual Slot"
    _rec_name = 'slot_date'

    slot_date = fields.Date(string='Slot Date')
    slot_ids = fields.One2many('appointment.schedual.slot.lines', 'slot_id', string="Slot Lines")
    
    _sql_constraints = [('slot_date_unique', 'UNIQUE(slot_date)', 'Error: Appointment slot must be unique!')]

    @api.model
    def create_appointment_slot(self,slot_date):
        slot_obj = self.env['appointment.schedual.slot']
        schedual_lines = self.env['appointment.schedual.lines']
        slot_line = self.env['appointment.schedual.slot.lines']

        weekday = slot_date.weekday()
        slot = slot_obj.create({'slot_date': slot_date.strftime("%m/%d/%Y")})
        #Create Slot lines with interval of 15 minutes.
        for line in schedual_lines.search([('dayofweek','=',str(weekday))]):
            sh, sm = str(line.hour_from).split('.')
            eh, em = str(line.hour_to).split('.')
            d = datetime.datetime.strptime(slot_date.strftime("%m/%d/%Y 00:00:00"), "%m/%d/%Y 00:00:00")

            start_date = d + datetime.timedelta(hours=int(sh), minutes=int(float(sm)*0.6))
            end_date = d + datetime.timedelta(hours=int(eh), minutes=int(float(em)*0.6))
            start = line.hour_from
            #Convert UTC to users local timezone and store data in UTC.
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            start_date = user_tz.localize(datetime.datetime.strptime(start_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(pytz.utc)
            start_date.replace(tzinfo=None)
            while (start < line.hour_to):
                start +=0.25
                end_date = start_date + datetime.timedelta(minutes=15)
                name = start_date.strftime("%H:%M") + ' - ' + end_date.strftime("%H:%M")
                slot_line.create({'name': name,'from_slot':start_date,'to_slot': end_date,'limit':5,'slot_id':slot.id})
                start_date = end_date

    # Cron for create weekly slot creation.
    @api.model
    def weekly_slot_create_cron(self):
        # get day of next week
        slot_obj = self.env['appointment.schedual.slot']
        next_slot = datetime.datetime.now().date() + datetime.timedelta(days=7)
        slot_found = slot_obj.search([('slot_date','=',next_slot.strftime("%m/%d/%Y"))])
        if slot_found:
                raise UserError(_("Appointment Slot exist for date %s." % start_date.strftime("%m/%d/%Y")))
        self.create_appointment_slot(next_slot)


class AppointmentSchedualSlotLines(models.Model):
    _name = "appointment.schedual.slot.lines"
    _description = "Appointment Schedual Slot Lines"
    #_order = 'dayofweek, hour_from'

    @api.model
    def _get_slot_name(self):
        return 'Slot'

    @api.multi
    @api.depends('appointment_ids')
    def _limit_count(self):
        for slot in self:
            slot.rem_limit = len(self.env['hms.appointment'].search([('schedual_slot_id','=',slot.id),('state','!=','canceled')]))

    name = fields.Char(string='name',default=_get_slot_name)
    from_slot = fields.Datetime(string='Starting Slot')
    to_slot = fields.Datetime(string='End Slot')
    limit = fields.Integer(string='Limit',default=5)
    rem_limit = fields.Integer(compute="_limit_count",string='Remaining Limit',store=True)
    slot_id = fields.Many2one('appointment.schedual.slot', string="Slot")
    appointment_ids = fields.One2many('hms.appointment', 'schedual_slot_id', string="Appointment")

    @api.onchange('from_slot')
    def on_change_from_slot(self):
        if self.name and self.from_slot: 
            self.name = 'Slot- ' + datetime.datetime.strptime(self.from_slot, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

    @api.onchange('to_slot')
    @api.depends('from_slot')
    def on_change_to_slot(self):
        if self.name and self.from_slot and self.to_slot: 
            self.name = 'Slot  ' + datetime.datetime.strptime(self.from_slot, "%Y-%m-%d %H:%M:%S").strftime("%H:%M") + ' - '+ datetime.datetime.strptime(self.to_slot, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")


class Appointment(models.Model):
    _inherit = 'hms.appointment'

    schedual_slot_id = fields.Many2one('appointment.schedual.slot.lines', string = 'Schedual Slot')
    booked_online = fields.Boolean('Booked Online')


