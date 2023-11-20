# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime

class ResCompany(models.Model):
    _inherit = "res.company"
    
    terms_consent_blood1 = fields.Text(string='Consent for Blood - Blood Components Transfusion (English) Part 1')
    terms_consent_blood2 = fields.Text(string='Consent for Blood - Blood Components Transfusion (English) Part 2')
    terms_consent_blood1_hi = fields.Text(string='Consent for Blood - Blood Components Transfusion (Hindi) Part 1')
    terms_consent_blood2_hi = fields.Text(string='Consent for Blood - Blood Components Transfusion (Hindi) Part 2')
    terms_consent_blood1_gj = fields.Text(string='Consent for Blood - Blood Components Transfusion (Gujarat) Part 1')
    terms_consent_blood2_gj = fields.Text(string='Consent for Blood - Blood Components Transfusion (Gujarat) Part 2')
    terms_consent_admission_en = fields.Text(string='General Consent for Admission Terms (English)')
    terms_consent_admission_hi = fields.Text(string='General Consent for Admission Terms (Hindi)')
    terms_consent_admission_gj = fields.Text(string='General Consent for Admission Terms (Gujarati)')
    terms_consent_form = fields.Text(string='Consent form in English')
    terms_consent_form_hi = fields.Text(string='Consent form in Hindi')
    terms_consent_form_gj = fields.Text(string='Consent form in Gujarati')

    

class ConsentForm(models.Model):
    _name = "consent.form"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "consent form"
    
    name = fields.Char(size=10, string='Consent', copy=False)
    inpatient_id = fields.Many2one("inpatient.registration", ondelete="cascade", string="Hospitalization")
    patient_id = fields.Many2one(related="inpatient_id.patient_id", string='Patient')
    language = fields.Selection(related="patient_id.language", string='Language')
    consent_date = fields.Datetime('Admission Date', required=True, default=fields.Datetime.now)
    nurse_id = fields.Many2one(related="inpatient_id.nurse_id", string='Unit Nurse')
    doctor_id = fields.Many2one(related="inpatient_id.primary_physician", string='Unit Doctor')
    relative_name = fields.Char(related="inpatient_id.relative_name",  string='Relative Name')
    relative_phone = fields.Char(string='Relative Phone')
    relative_street = fields.Char(string='Relative Street')
    relative_street2 =fields.Char(string='Relative Street 2')
    relative_state = fields.Many2one('res.country.state', string='Relative State')
    relation = fields.Char(string='Relationship')
    state = fields.Selection([('draft','Draft'),('done','Done'),('cancel','Cancel')], default="draft", string="State")
    remark = fields.Text('Remark')
    area_id = fields.Many2one('res.area', 'Area')
    city_id = fields.Many2one('res.city', 'City')
    zip = fields.Char('Zip')

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('consent.form') or ''
        return super(ConsentForm, self).create(values)

    @api.multi
    def button_done(self):
        self.state = 'done'

    @api.multi
    def button_cancel(self):
        self.state = 'cancel'

    @api.onchange('area_id')
    def onchange_area(self):
        if self.area_id:
            self.city_id = self.area_id.city_id.id or False
            self.relative_state = self.area_id.city_id.state_id.id
            self.zip = self.area_id.zip
            
    
class Hospitalization(models.Model):
    _inherit = "inpatient.registration"
    
    @api.multi
    def action_button_consent_form(self):
        return {
            'name': _(self.name),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'consent.form',
            'domain': [('inpatient_id','=',self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_inpatient_id': self.id},
        }
