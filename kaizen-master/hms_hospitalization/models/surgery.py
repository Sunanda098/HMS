# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Add to the Past Surgeries in hms.patient class.



class PastSurgeries(models.Model):
    _name = "past.surgeries"
    _description = "Past Surgeries"
   
    result= fields.Char(string='Outcome')
    date= fields.Date(string='Date')
    hosp_or_doctor= fields.Char(string='Hospital/Doctor')
    description= fields.Char(string='Description', size=128)
    past_surgery_id= fields.Many2one('hms.patient', ondelete="restrict", string='Surgery ID')
    appointment_id= fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
# Add to the Medical patient_data class (hms.patient) the surgery field.

class IndimediPatient (models.Model):
    _inherit = "hms.patient"
    
    surgery= fields.Many2many ('hms_surgery', 'patient_surgery_rel','surgery_id','patient_id', string='Fusion Surgeries')
    past_surgeries_ids= fields.One2many('past.surgeries', 'past_surgery_id', string='Past Surgeries')
    age_years = fields.Integer(string='Age in Year')
    
    @api.onchange('dob')
    def onchange_dob(self):
        if self.dob:
            b_date = datetime.strptime(self.dob, '%Y-%m-%d')
            self.age_years = relativedelta(datetime.now(), b_date).years
        return super(IndimediPatient, self).onchange_dob()
                
    @api.multi
    def action_hospitalization(self):                
        return {
            'name': _('Hospitalizations'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'inpatient.registration',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id','=',self.id)],
            'context': {'default_patient_id': self.id},                        
        }

