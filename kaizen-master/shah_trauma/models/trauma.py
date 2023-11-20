# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime

    

class Xray(models.Model):
    _name = "trauma.xray"
   
    name = fields.Char(string='Xray')

class Advice(models.Model):
    _name = "trauma.advice"
   
    name = fields.Char(string='Advice')


class HeadInjury(models.Model):
    _name ='head.injury'

    name = fields.Char(string='History of head injury')

class HistoryLoss(models.Model):
    _name ='history.loss'

    name = fields.Char(string='History of loss of consciousness,vomiting or bleeding from ear,nose or mouth')
    
class ShahTrauma(models.Model):
    _name = "shah.trauma"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Shah Trauma"
    
    name = fields.Char(size=10, string='Name', copy=False)
    inpatient_id = fields.Many2one("hms.appointment", ondelete="cascade", string="Appointment")
    patient_id = fields.Many2one(related="inpatient_id.patient_id", string='Patient')
    date_trauma = fields.Datetime('Date', required=True, default=fields.Datetime.now)
    ho = fields.Text('H/O')
    head_injury_id = fields.Many2one('head.injury', string='Head Injury')
    history_loss_id = fields.Many2one('history.loss', string='History of Loss')
    consciousness = fields.Char('Consciousness')
    pulse = fields.Char('Pulse')
    bp = fields.Char("B.P.")
    resp = fields.Char('Res.')
    orientation = fields.Char("Orientation")
    temp = fields.Char('Temp.')
    co = fields.Text('C/O')
    oe = fields.Text('O/E')
    mri = fields.Text('CT/MRI')
    lab = fields.Text('Labortory')
    alcohol = fields.Boolean('Influence Of Alcohol') 
    legal = fields.Boolean('Medico-Legal Case') 
    xray_id =  fields.Many2one('trauma.xray', string='Xray')
    advice_id = fields.Many2one('trauma.advice', string='Advice')
    state = fields.Selection([('draft','Draft'),('done','Done'),('cancel','Cancel')], default="draft", string="State")
    
    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('shah.trauma') or ''
        return super(ShahTrauma, self).create(values)

    def get_name(self,obj):
        name = []
        if obj.patient_id.first_name:
            name.append(str(obj.patient_id.first_name))
            if obj.patient_id.middel_name:
                name.append(str(obj.patient_id.middel_name[0]))
            if obj.patient_id.last_name:
                name.append(str(obj.patient_id.last_name))
            return ' '.join(name)

    @api.multi
    def button_done(self):
        self.state = 'done'

    @api.multi
    def button_cancel(self):
        self.state = 'cancel'        
    
class Appointment(models.Model):
    _inherit = "hms.appointment"

    @api.multi
    def action_trauma(self):
        return {
            'name': _(self.name),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'shah.trauma',
            'domain': [('inpatient_id','=',self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_inpatient_id': self.id,'default_patient_id':self.patient_id.id},
        }

class Hospitalization(models.Model):
    _inherit ='inpatient.registration'

    def _get_history(self):
        for app in self:
            if app.appointment_id:
                history = ""
                for appointment in self.env['shah.trauma'].search([('inpatient_id', '=', app.appointment_id.id)]):
                    history += "<table class='table table-condensed'>"
                    if appointment.date_trauma:
                        history += _("<tr><td></td><td><b>Date:</b>%s</td><td></td></tr>")%(datetime.strptime(appointment.date_trauma,'%Y-%m-%d  %H:%M:%S'))
                    history += _("<tr><td><b>Head Injury:</b>%s</td>")%(appointment.head_injury_id.name or '')
                    history += _("<td><b>History of Loss:</b>%s</td></tr>")%(appointment.history_loss_id.name or '')
                    history += _("<tr><td><b>Consciousness:</b>%s</td>")%(appointment.consciousness or '')
                    history += _("<td><b>Pulse:</b>%s</td>")%(appointment.pulse or '')
                    history += _("<td><b>Bp:</b>%s</td></tr>")%(appointment.bp or '')
                    history += _("<tr><td><b>Resp:</b>%s</td>")%(appointment.resp or '')
                    history += _("<td><b>Orientation:</b>%s</td>")%(appointment.orientation or '')
                    history += _("<td><b>Temp:</b>%s</td></tr>")%(appointment.temp or '')
                    history += _("<tr><td><b>Alcohol:</b>%s</td>")%(appointment.alcohol or '')
                    history += _("<td><b>Legal:</b>%s</td></tr>")%(appointment.legal or '')
                    history += _("<tr><td><b>C/O:</b>%s</td>")%(appointment.co or '')
                    history += _("<td><b>O/E:</b>%s</td></tr>")%(appointment.oe or '')
                    history += _("<tr><td><b>MRI:</b>%s</td>")%(appointment.mri or '')
                    history += _("<td><b>Lab:</b>%s</td></tr>")%(appointment.lab or '')
                    history += _("<tr><td><b>H/O:</b>%s</td></tr>")%(appointment.ho or '')
                    history += _("<tr><td><b>X-Ray:</b>%s</td></tr>")%(appointment.xray_id.name or '')
                    history += _("<tr><td><b>Advice:</b>%s</td></tr>")%(appointment.advice_id.name or '')
                    history += _("</table></td></tr>")
                app.clinincal_history = history

    clinincal_history = fields.Html(compute='_get_history', string='Clinical History')
    