# -*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models ,_
from openerp.exceptions import UserError


class IndiPatient(models.Model):
    _inherit='hms.patient'
    
    fertile = fields.Boolean(string ='Infertility', help="Check if patient is in fertile age")
    currently_pregnant = fields.Boolean(string ='Currently Pregnant')
    menarche = fields.Integer(string ='Menarche age')
    menopausal = fields.Boolean(string ='Menopausal')
    menopause = fields.Integer(string ='Menopause age')
    dispareunia_sup = fields.Boolean(string ='Dyspareunia Superficial')
    dispareunia_deep = fields.Boolean(string ='Dyspareunia Deep')
    gravida = fields.Integer(string='Gravida', help="Number of pregnancies")
    premature = fields.Integer(string='Premature', help="Premature Deliveries")
    abortions = fields.Integer(string='Abortions')
    stillbirths = fields.Integer(string='Stillbirths')
    menstrual_history = fields.One2many('hms.patient.menstrual_history', 'name', string = 'Menstrual History')
    pregnancy_history = fields.One2many('hms.patient.pregnancy', 'name', string='Pregnancies')
    prenatal_evaluations = fields.One2many('hms.patient.prenatal.evaluation', 'name', string='Prenatal Evaluations')
    mammography = fields.Boolean(string='Mammography', help="Check if the patient does periodic mammographys")
    mammography_last = fields.Date(string='Last mammography', help="Enter the date of the last mammography")
    breast_self_examination = fields.Boolean(string='Breast self-examination', help="Check if patient does and knows how to self examine her breasts")
    pap_test = fields.Boolean(string='PAP test',  help="Check if patient does periodic cytologic pelvic smear screening")
    pap_test_last = fields.Date(string='Last PAP test', help="Enter the date of the last Papanicolau test")
    colposcopy = fields.Boolean(string='Colposcopy', help="Check if the patient has done a colposcopy exam")
    colposcopy_last = fields.Date(string='Last colposcopy', help="Enter the date of the last colposcopy")
    full_term = fields.Integer(string='Full Term', help="Full term pregnancies")
    mammography_history = fields.One2many('hms.patient.mammography_history', 'name', string='Mammography History')
    pap_history = fields.One2many('hms.patient.pap_history', 'name', string='PAP smear History')
    colposcopy_history = fields.One2many('hms.patient.colposcopy_history', 'name', string='Colposcopy History')
    husband_name = fields.Char("Husband's Name")
    husband_edu = fields.Char("Husband's Education")
    husband_business = fields.Char("Husband's Business")
    education = fields.Char("Patient Education")
    #For Basic Medical Info
    hb = fields.Float(string='HB')
    urine = fields.Char('Urine')
    rbs = fields.Float('RBS')
    screatinine = fields.Float('S Creatinine')
    hiv = fields.Selection([('negative','Negative'),('positive','Positive')],"HIV")
    hbsag = fields.Selection([('negative','Negative'),('positive','Positive')],"HBSAG")
    sonography_pelvis_ids = fields.One2many('hms.appointment.sonography.pelvis', 'patient_id', string='Sonography Pelvis Reports')
    sonography_follical_ids = fields.One2many('hms.appointment.sonography.follical', 'patient_id', string='Sonography Follical Reports')
    sonography_obstetric_ids = fields.One2many('hms.appointment.sonography.obstetric', 'patient_id', string='Sonography Obstetric Reports')
    aml = fields.Char('AML',size=64)
    other = fields.Char('Other')
    dymenorreha = fields.Boolean(string='Dymenorreha')
    menorrhagia = fields.Boolean(string='Menorrhagia')
    oligomenorrhea = fields.Boolean(string='Oligomenorrhea')
    leucorrhoea = fields.Boolean(string='Leucorrhoea')
    urinary_problem = fields.Boolean(string='Urinary Problem')
    tl_done = fields.Selection([
                ('yes', 'Yes'),
                ('no', 'No'),
                ], string='TL/Done')
    amenorrhea = fields.Selection([
                ('primary', 'Primary'),
                ('secondary', 'Secondary'),
                ], string='Amenorrhea')

class PatientMenstrualHistory(models.Model):
    _name = 'hms.patient.menstrual_history'
    _description =  'Menstrual History'
    
    name = fields.Many2one('hms.patient',string ='Patient')
    lmp = fields.Date(string='LMP', help="Last Menstrual Period", required=True)
    lmp_length = fields.Integer(string='Length', required=True)
    frequency = fields.Selection([('amenorrhea', 'amenorrhea'),
                ('oligomenorrhea', 'oligomenorrhea'),
                ('eumenorrhea', 'eumenorrhea'),
                ('polymenorrhea', 'polymenorrhea'),
                ], string='frequency', sort=False)
    volume = fields.Selection([('amenorrhea', 'amenorrhea'),
                ('hypomenorrhea', 'hypomenorrhea'),
                ('normal', 'normal'),
                ('menorrhagia', 'menorrhagia'),
                ], string='volume', sort=False)
    is_regular = fields.Boolean(string ='Regular')
    dysmenorrhea = fields.Boolean(string ='Dysmenorrhea')
    
    
class PatientPregnancy(models.Model):
    _name = 'hms.patient.pregnancy'
    _description = 'Patient Pregnancy'
    
    @api.multi
    def _get_pregnancy_data(self,name, args):
        if name == 'pdd':
            return self.lmp + datetime.timedelta(days=280)
        if name == 'pregnancy_end_age':
            if self.pregnancy_end_date:
                gestational_age = datetime.datetime.date(
                    self.pregnancy_end_date) - self.lmp
                return (gestational_age.days) / 7
        return 2
    
    
    name = fields.Many2one('hms.patient', string='Patient ID')
    gravida = fields.Integer(string='Pregnancy #')
    lmp = fields.Date(string='Last Menstrual Period', help="Last Menstrual Period", required=True)
    current_pregnancy = fields.Boolean(string='Current Pregnancy', help='This field marks the current pregnancy')
    fetuses = fields.Integer(string='Fetuses', required=True)
    warning = fields.Boolean(string='Warn', help='Check this box if this is pregancy is or was NOT normal')
    pdd = fields.Date(compute=_get_pregnancy_data, string='Pregnancy Due Date')
    prenatal_evaluations = fields.One2many('hms.patient.prenatal.evaluation', 'name', string='Prenatal Evaluations')
    perinatal = fields.One2many('hms.perinatal', 'name', string='Perinatal Info')
    puerperium_monitor = fields.One2many('hms.puerperium.monitor', 'name', string='Puerperium monitor')
    monozygotic = fields.Boolean('Monozygotic')
    pregnancy_end_result = fields.Selection([
                                ('live_birth', 'Live birth'),
                                ('abortion', 'Abortion'),
                                ('stillbirth', 'Stillbirth'),
                                ('status_unknown', 'Status unknown'),
                                ], string='Result', sort=False,)
    pregnancy_end_date = fields.Datetime(string='End of Pregnancy')
    iugr = fields.Selection([
                ('symmetric', 'Symmetric'),
                ('assymetric', 'Assymetric'),
                ], string='IUGR', sort=False)
                
                
class OemedicalPerinatal(models.Model):
    _name = 'hms.perinatal'
    _description =  'Perinatal Information'
    
    name = fields.Many2one('hms.patient', string='Perinatal Infomation')
    admission_code = fields.Char(string='Admission Code', size=64)
    gravida_number = fields.Integer(string='Gravida #')
    abortion = fields.Boolean(string='Abortion')
    admission_date = fields.Datetime(string='Admission date', help="Date when she was admitted to give birth")
    prenatal_evaluations = fields.Integer(string='Prenatal evaluations', help="Number of visits to the doctor during pregnancy")
    start_labor_mode = fields.Selection([
    ('n', 'Normal'),
    ('i', 'Induced'),
    ('c', 'c-section'),
    ], string='Labor mode', select=True)
    gestational_weeks = fields.Integer(string='Gestational weeks')
    gestational_days = fields.Integer(string='Gestational days')
    fetus_presentation = fields.Selection([
            ('n', 'Correct'),
            ('o', 'Occiput / Cephalic Posterior'),
            ('fb', 'Frank Breech'),
            ('cb', 'Complete Breech'),
            ('t', 'Transverse Lie'),
            ('t', 'Footling Breech'),
            ], string='Fetus Presentation', select=True)
    dystocia = fields.Boolean(string='Dystocia')
    laceration = fields.Selection([
            ('perineal', 'Perineal'),
            ('vaginal', 'Vaginal'),
            ('cervical', 'Cervical'),
            ('broad_ligament', 'Broad Ligament'),
            ('vulvar', 'Vulvar'),
            ('rectal', 'Rectal'),
            ('bladder', 'Bladder'),
            ('urethral', 'Urethral'),
            ],string='Lacerations', sort=False)
    hematoma = fields.Selection([
            ('vaginal', 'Vaginal'),
            ('vulvar', 'Vulvar'),
            ('retroperitoneal', 'Retroperitoneal'),
            ], string='Hematoma', sort=False)
    placenta_incomplete = fields.Boolean(string='Incomplete Placenta')
    placenta_retained = fields.Boolean(string='Retained Placenta')
    abruptio_placentae = fields.Boolean(string='Abruptio Placentae', help='Abruptio Placentae')
    episiotomy = fields.Boolean(string='Episiotomy')
    vaginal_tearing = fields.Boolean(string='Vaginal tearing')
    forceps = fields.Boolean(string='Use of forceps')
    monitoring = fields.One2many('hms.perinatal.monitor', 'name', string='Monitors')
    puerperium_monitor = fields.One2many('hms.puerperium.monitor', 'name',string='Puerperium monitor')
    #medications = fields.One2many('hms.patient.medication','patient_id', string='Medications')
    dismissed = fields.Datetime(string='Dismissed from hospital')
    place_of_death = fields.Selection([
    ('ho', 'Hospital'),
    ('dr', 'At the delivery room'),
    ('hh', 'in transit to the hospital'),
    ('th', 'Being transferred to other hospital'),
    ],string='Place of Death')
    mother_deceased = fields.Boolean(string='Deceased', help="Mother died in the process")
    notes = fields.Text(string='Notes')


class PrenatalEvaluation(models.Model):

    _name = 'hms.patient.prenatal.evaluation'
    _description =  'Prenatal and Antenatal Evaluations'

    @api.multi
    def _get_patient_evaluation_data(self, field_name, args):
        result = dict([(i, {}.fromkeys(field_names, 0.0)) for i in self.ids])
        return 20

    name = fields.Many2one('hms.patient.pregnancy', string='Patient Pregnancy')
    gestational_weeks = fields.Float(compute=_get_patient_evaluation_data, method=True , string="Gestational Weeks")
    gestational_days = fields.Integer(compute=_get_patient_evaluation_data, method=True , string='Gestational days')
    hypertension = fields.Boolean(string='Hypertension', help='Check this box if the mother has hypertension')
    preeclampsia = fields.Boolean(string='Preeclampsia', help='Check this box if the mother has pre-eclampsia')
    overweight = fields.Boolean(string='Overweight', help='Check this box if the mother is overweight or obesity')
    diabetes = fields.Boolean(string='Diabetes', help='Check this box if the mother has glucose intolerance or diabetes')
    invasive_placentation = fields.Selection([
        ('normal', 'Normal decidua'),
        ('accreta', 'Accreta'),
        ('increta', 'Increta'),
        ('percreta', 'Percreta'),
        ], string='Placentation')
    placenta_previa = fields.Boolean(string='Placenta Previa')
    vasa_previa = fields.Boolean(string='Vasa Previa')
    fundal_height = fields.Integer(string='Fundal Height', help="Distance between the symphysis pubis and the uterine fundus (S-FD) in cm")
    fetus_heart_rate = fields.Integer(string='Fetus heart rate', help='Fetus heart rate')
    efw = fields.Integer(string='EFW', help="Estimated Fetal Weight")
    fetal_bpd = fields.Integer(string='BPD', help="Fetal Biparietal Diameter")
    fetal_ac = fields.Integer(string='AC', help="Fetal Abdominal Circumference")
    fetal_hc = fields.Integer(string='HC', help="Fetal Head Circumference")
    fetal_fl = fields.Integer(string='FL', help="Fetal Femur Length")
    oligohydramnios = fields.Boolean(string='Oligohydramnios')
    polihydramnios = fields.Boolean(string='Polihydramnios')
    iugr = fields.Boolean(string='IUGR', help="Intra Uterine Growth Restriction")

class PuerperiumMonitor(models.Model):

    _name = 'hms.puerperium.monitor'
    _description = 'Puerperium Monitor'

    name = fields.Many2one('hms.patient', string='Patient ID')
    date = fields.Datetime(string='Date and Time', required=True)
    systolic = fields.Integer(string='Systolic Pressure')
    diastolic = fields.Integer(string='Diastolic Pressure')
    frequency = fields.Integer(string='Heart Frequency')
    lochia_amount = fields.Selection([
       ('n', 'normal'),
    ('e', 'abundant'),
    ('h', 'hemorrhage'),
    ],string='Lochia amount', select=True)
    lochia_color = fields.Selection([
    ('r', 'rubra'),
    ('s', 'serosa'),
    ('a', 'alba'),
    ], string='Lochia color', select=True)
    lochia_odor = fields.Selection([
    ('n', 'normal'),
    ('o', 'offensive'),
    ], string='Lochia odor', select=True)
    uterus_involution = fields.Integer(string='Fundal Height', help="Distance between the symphysis pubis and the uterine fundus (S-FD) in cm")
    temperature = fields.Float(string='Temperature')

class PerinatalMonitor(models.Model):
    
    _name = 'hms.perinatal.monitor'
    _description = 'Perinatal monitor'
    
    name = fields.Many2one('hms.patient', string='patient')
    date = fields.Datetime(string='Date and Time')
    systolic = fields.Integer(string='Systolic Pressure')
    diastolic = fields.Integer(string='Diastolic Pressure')
    contractions = fields.Integer(string='Contractions')
    frequency = fields.Integer(string='Mother\'s Heart Frequency')
    dilation = fields.Integer(string='Cervix dilation')
    f_frequency = fields.Integer(string='Fetus Heart Frequency')
    meconium = fields.Boolean(string='Meconium')
    bleeding = fields.Boolean(string='Bleeding')
    fundal_height = fields.Integer(string='Fundal Height')
    fetus_position = fields.Selection([
    ('n', 'Correct'),
    ('o', 'Occiput / Cephalic Posterior'),
    ('fb', 'Frank Breech'),
    ('cb', 'Complete Breech'),
    ('t', 'Transverse Lie'),
    ('t', 'Footling Breech'),
    ], string='Fetus Position', select=True)

class PatientMammographyHistory(models.Model):

    _name = 'hms.patient.mammography_history'
    _description =  'Mammography History'

    name = fields.Many2one('hms.patient', string='Patient', readonly=True, required=True)
    last_mammography = fields.Date(string='Date', help="Last Mammography", required=True)
    result = fields.Selection([
    ('normal', 'normal'),
    ('abnormal', 'abnormal'),
    ], string='Result', help="Please check the lab test results if the module is installed", sort=False)
    comments = fields.Char(string='Remarks')



class PatientPAPHistory(models.Model):

    _name = 'hms.patient.pap_history'
    _description =  'PAP Test History'

    name = fields.Many2one('hms.patient', string='Patient', readonly=True, required=True)
    last_pap = fields.Date(string='Date', help="Last Papanicolau", required=True)
    result = fields.Selection([
            ('negative', 'Negative'),
            ('c1', 'ASC-US'),
            ('c2', 'ASC-H'),
            ('g1', 'ASG'),
            ('c3', 'LSIL'),
            ('c4', 'HSIL'),
            ('g4', 'AIS'),
            ], string='Result', help="Please check the lab results if the module is installed")
    comments = fields.Char(string='Remarks')


class PatientColposcopyHistory(models.Model):

    _name = 'hms.patient.colposcopy_history'
    _description =  'Colposcopy History'
    
    name = fields.Many2one('hms.patient', string='Patient', readonly=True, required=True)
    last_colposcopy = fields.Date(string='Date', help="Last colposcopy", required=True)
    result = fields.Selection([
                    ('normal', 'normal'),
                    ('abnormal', 'abnormal'),
                    ], string='Result', help="Please check the lab test results if the module is installed", sort=False)
    comments = fields.Char(string='Remarks')
    
    
# class diet_plan(models.Model):
#     _name = "diet.plan"
    
#     name = fields.Char(string='Name', required=True)
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:   
