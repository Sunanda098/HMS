# -*- coding: utf-8 -*-

import time
from datetime import datetime
from openerp import api, fields, models, _
from datetime import datetime, timedelta as td

hours = [
            ('0', '00'),
            ('1', '01'),
            ('2', '02'),
            ('3', '03'),
            ('4', '04'),
            ('5', '05'),
            ('6', '06'),
            ('7', '07'),
            ('8', '08'),
            ('9', '09'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('19', '19'),
            ('20', '20'),
            ('21', '21'),
            ('22', '22'),
            ('23', '23'),
]

minutes = [
            ('0', '00'),
            ('5', '05'),
            ('10', '10'),
            ('15', '15'),
            ('20', '20'),
            ('25', '25'),
            ('30', '30'),
            ('35', '35'),
            ('40', '40'),
            ('45', '45'),
            ('50', '50'),
            ('55', '55'),
]

class SystemicAbdominalExamination(models.Model):
    _name = "systemic.abdominal.examination"
    
    date = fields.Datetime(string='Date',default=fields.Datetime.now)
    bp = fields.Char(string='B.P')
    weight = fields.Float(string='Weight')
    pa = fields.Char(string='P/A')
    remarks = fields.Char(string='Remarks', size=128)
    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
    patient_id = fields.Many2one("hms.patient", related='appointment_id.patient_id',string="Name", store=True)


class SystemicVeginalExamination(models.Model):
    _name = "systemic.veginal.examination"
    
    date = fields.Datetime(string='Date',default=fields.Datetime.now)
    bp = fields.Char(string='B.P')
    weight = fields.Float(string='Weight')
    pv = fields.Char(string='P/V')
    remarks = fields.Char(string='Remarks', size=128)
    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
    patient_id = fields.Many2one("hms.patient", related='appointment_id.patient_id',string="Name", store=True)


class SystemicRectalExamination(models.Model):
    _name = "systemic.rectal.examination"
    
    date = fields.Datetime(string='Date',default=fields.Datetime.now)
    bp = fields.Char(string='B.P')
    weight = fields.Float(string='Weight')
    pr = fields.Char(string='P/R')
    remarks = fields.Char(string='Remarks', size=128)
    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
    patient_id = fields.Many2one("hms.patient", related='appointment_id.patient_id',string="Name", store=True)
 

class Appointment(models.Model):
    _inherit = 'hms.appointment'
    
    @api.one
    def copy(self,default=None):
        default.update({'validity_status':'tobe'})
        return super(Appointment,self).copy(default)
            
    @api.onchange('appointment_date')
    def onchange_appointment_date(self):
        """On change of appointment date validity date set after 7 days"""
        if self.appointment_date:
            validity_date = datetime.Datetime.fromtimestamp(time.mktime(time.strptime(self.appointment_date,"%Y-%m-%d %H:%M:%S")))
            validity_date = validity_date+datetime.td(days=7)
            return {'value': {'appointment_validity_date':str(validity_date)}}
        return {}

    @api.multi
    def print_medical_advice(self):
        return self.env['report'].get_action(self,'hms_gynec.report_indimedi_medical_advice')


    user_id = fields.Many2one('res.users', ondelete="cascade", string='Created By', readonly=True, states={'draft': [('readonly', False)]})
    patient_id = fields.Many2one('hms.patient', ondelete="restrict", string='Patient', required=True, select=True, help='Patient Name')
    sex = fields.Selection(related='patient_id.sex', readonly=True, string='Sex')
    name = fields.Char(size=256, string='Appointment', readonly=True)
    appointment_date = fields.Datetime(string='Appointment Date',select=True, states={'draft': [('readonly', False)]})
    appointment_day = fields.Datetime(string='Creation Date',default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    appointment_hour = fields.Selection(hours, string='Hour')
    appointment_minute = fields.Selection(minutes,string='Minute')
    history_of_present_illness = fields.Text(string='History of Present Illness')
    notess = fields.Text(string='Notes')
    highlight = fields.Text(string='Notes')
    doctor = fields.Many2one('hms.physician', ondelete="restrict", string='Doctor', select=True, help='Physician\'s Name')
    doc_user = fields.Many2one('res.users', related='doctor.user_id', readonly=False, store=True, string='Packaging Type')
    alias = fields.Char(size=256, string='Alias')
    appointment_type = fields.Selection([('ambulatory', 'Ambulatory'),('outpatient', 'Outpatient'),('inpatient', 'Inpatient')], string='Type')          
    urgency = fields.Selection([
        ('a', 'Normal'),
        ('b', 'Urgent'),
        ('c', 'Medical Emergency') ],
        string='Urgency Level',default='a')
    speciality = fields.Many2one('hms.specialty', ondelete="cascade", string='Speciality', help='Medical Speciality / Sector')
    history_ids = fields.One2many('hms.appointment.history', 'appointment_id_history', string='History lines', states={'start': [('readonly', True)]})
    appointment_validity_date = fields.Datetime(string='Validity Date')
    validity_status = fields.Selection([('invoiced','Invoiced'),('tobe','To be Invoiced')],string='Status',default=lambda *a: 'tobe')
    lmp = fields.Date(string='LMP', help="Last Menstrual Period")
    induction = fields.Char(string='Induction')
    induction_remarks = fields.Char(string='Remarks', size=128)
    hsg = fields.Char(string='HSG')
    hsg_remarks = fields.Char(string='Remarks', size=128)
    follicular_study = fields.Char(string='Follicular Study')
    follicular_study_remarks = fields.Char(string='Remarks', size=128)
    dhl = fields.Char(string='DHL')
    dhl_remarks = fields.Char(string='Remarks', size=128)
    iui = fields.Char(string='IUI')
    iui_remarks = fields.Char(string='Remarks', size=128)
    ivf = fields.Char(string='IVF')
    ivf_remarks = fields.Char(string='Remarks', size=128)
    abdominal_examination_ids = fields.One2many('systemic.abdominal.examination', 'appointment_id',string= 'Abdominal Examinations')
    veginal_examination_ids = fields.One2many('systemic.veginal.examination', 'appointment_id', string='Per Vaginal Examinations')
    rectal_examination_ids = fields.One2many('systemic.rectal.examination', 'appointment_id', string='Per Rectal Examinations')
    #sms remainder 
    is_sms = fields.Boolean(string="Is SMS",default=False)
    entry = fields.Selection([('walking','Walking'),('future','Future')],string='Type of Entry',default='walking')
    appointment_reason_id = fields.Many2one("hms.reason", ondelete="cascade", string="Reason")
    appointment_follow = fields.Integer(string="Follow Up Date")

    @api.onchange('doctor')           
    def onchange_doctor(self):
        if self.doctor:    
            return {'value': {'speciality': self.doctor.specialty.id, 'product_id': self.doctor.consul_service.id}}
            
    @api.multi      
    def unlink(self):
        """Allows to delete in draft state"""
        for rec in self:
            if rec.state not in ['draft']:
                raise osv.except_osv(_('Invalid Action!'), _('Appointment can be delete only in Draft state.'))
        return super(OeMedicalAppointment, self).unlink()
        
    @api.model   
    def default_get(self, fields):
        result = super(Appointment, self).default_get(fields)
        result.update({'consultation_type':'consultation','create_uid':self.env.uid,'create_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return result

class OeMedicalAppointmentHistory(models.Model):
    _name = 'hms.appointment.history'

    appointment_id_history = fields.Many2one('hms.appointment', ondelete="cascade", string='History')
    date = fields.Datetime(string='Date and Time')
    name = fields.Many2one('res.users', string='User', ondelete="cascade")
    action = fields.Text(string='Action')
    


class OeMedicalAppointmentSonographyPelvis(models.Model):
    _name = 'hms.appointment.sonography.pelvis'

    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
    patient_id = fields.Many2one("hms.patient",related='appointment_id.patient_id', string="Name", store=True)
    date = fields.Date(string='Date',default=fields.Date.context_today)
    lmp = fields.Date('LMP', help="Last Menstrual Period", required=True)
    uterus = fields.Char('Uterus')
    uterus_size = fields.Char('Uterus size')
    endometrial_thickness = fields.Char('Endometrial Thickness')
    left_ovary_size = fields.Char('Left Ovary size')
    right_ovary_size = fields.Char('Rigth Ovary size')
    conclusion = fields.Text('Conclusion')

    @api.multi
    def print_sono_elvis_report(self):
        return self.env['report'].get_action(self,'hms_gynec.report_sono_pelvis')


class OeMedicalAppointmentSonographyFollicalLine(models.Model):
    _name = 'sonography.follical.line'

    follical_id = fields.Many2one('hms.appointment.sonography.follical', ondelete="cascade", string='Report')
    date = fields.Date(string='Date',default=fields.Date.context_today)
    cycle_day = fields.Char(string='DAY/CYCLE')
    left_ovary_size = fields.Char(string='LT OVARY')
    right_ovary_size = fields.Char(string='RT OVARY')
    endometriulm = fields.Char(string='ENDOMETRIULM')
    curvical_mucus = fields.Char(string='CURVICAL MUCUS')


class OeMedicalAppointmentSonographyFollical(models.Model):
    _name = 'hms.appointment.sonography.follical'

    date = fields.Date(string='Date',default=fields.Date.context_today)
    lmp = fields.Date('LMP', help="LMP")
    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
    patient_id = fields.Many2one('hms.patient',related="appointment_id.patient_id", string="Name", store=True)
    line_ids = fields.One2many('sonography.follical.line', 'follical_id', 'Sonography Obstetric Reports')
    conclusion = fields.Text('Conclusion')
    advice = fields.Text('Advice')

    @api.multi
    def print_sono_follical_report(self):
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        return self.env['report'].get_action(self,'hms_gynec.report_sono_follical')



class OeMedicalAppointmentSonographyObstetric(models.Model):
    _name = 'hms.appointment.sonography.obstetric'

    date = fields.Date(string='Date',default=fields.Date.context_today)
    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", string='Appointment')
    patient_id = fields.Many2one("hms.patient",related='appointment_id.patient_id', string="Name", store=True)
    age = fields.Char(related='patient_id.age',string='Age')
    lmp = fields.Date(string='LMP', help="Last Menstrual Period", required=True)
    fetal_movement = fields.Char(string='Fetal Movement')
    cardiac_activity = fields.Boolean(string='Cardiac Activity')
    fhr = fields.Char(string='F.H.R')
    fetues = fields.Selection([
        ('single', 'Single'),
        ('twins', 'Twins'),
    ], string='No. Of Fetues', select=True)
    presentation = fields.Selection([
        ('vertex', 'Vertex'),
        ('breech', 'Breech'),
        ('variable', 'Variable'),
        ('oblique', 'Oblique'),
        ('transverse', 'Transverse'),
        ], string='Presentation', select=True)
    placenta = fields.Selection([
        ('fundal', 'Fundal'),
        ('anterior', 'Anterior'),
        ('posterior', 'Posterior'),
        ('previa', 'Previa'),
        ('lawline', 'Lawline'),
        ], string='Placenta', select=True)
    amniotic_fluid = fields.Selection([
        ('adequate', 'Adequate'),
        ('less', 'Less'),
        ], string='Amniotic Fluid', select=True)
    fluid_less = fields.Char(string='Fluid Vallue')
    #Fetal Parameters
    bpd = fields.Char(string='B.P.D')
    bpd_days = fields.Char(string='B.P.D Days')
    bpd_weeks = fields.Char(string='B.P.D Weeks')
    fl = fields.Char(string='F.L')
    fl_days = fields.Char(string='F.L Days')
    fl_weeks = fields.Char(string='F.L Weeks')
    hc = fields.Char(string='H.C')
    hc_days = fields.Char(string='H.C Days')
    hc_weeks = fields.Char(string='H.C Weeks')
    ac = fields.Char(string='A.C')
    ac_days = fields.Char(string='A.C Days')
    ac_weeks = fields.Char(string='A.C Weeks')
    crl = fields.Char(string='CRL')
    crl_days = fields.Char(string='CRL Days')
    crl_weeks = fields.Char(string='CRL Weeks')
    fetal_age = fields.Char(string='Average Estimated Fetal Age')
    edd = fields.Date(string='EDD')
    fetal_weight = fields.Char(string='Estimated Fetal Weight')
    cerrvix_lenght = fields.Char(string='Cervix Length')
    cerrvix_width = fields.Char(string='Cervix Width')
    internalos = fields.Char(string='Internal OS')
    sono_fetal_anomaly = fields.Char(string='Any Sonographically detectable fetal anomaly')
    impression = fields.Text(string='Impression')

    @api.multi
    def print_sono_obstetric_report(self):
        return self.env['report'].get_action(self,'hms_gynec.report_sono_obstetric')

class OeMedicalAppointment(models.Model):
    _inherit = "hms.appointment"

    sonography_obstetric_ids = fields.One2many('hms.appointment.sonography.obstetric', 'appointment_id',string='Sonography Obstetric Reports')
    sonography_pelvis_ids = fields.One2many('hms.appointment.sonography.pelvis', 'appointment_id',string='Sonography Pelvis Reports')
    sonography_follical_ids = fields.One2many('hms.appointment.sonography.follical', 'appointment_id',string='Sonography Follical Reports')

class IndimediPatient (models.Model):
    _inherit = "hms.patient"
    
    sonography_obstetric_ids = fields.One2many('hms.appointment.sonography.obstetric', 'patient_id',string='Sonography Obstetric Reports')
    sonography_pelvis_ids = fields.One2many('hms.appointment.sonography.pelvis', 'patient_id',string='Sonography Pelvis Reports')
    sonography_follical_ids = fields.One2many('hms.appointment.sonography.follical', 'patient_id',string='Sonography Follical Reports')
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
