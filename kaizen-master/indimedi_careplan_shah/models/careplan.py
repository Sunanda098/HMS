 # -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from datetime import datetime ,date ,timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT
from openerp.exceptions import UserError, ValidationError

selection_time = [
    ('8_9', '08-09 AM'),('9_10','09-10 AM'),
    ('10_11','10-11 AM'),('11_12','11-12 AM'),
    ('12_13','12-01 PM'),('13_14','01-02 PM'),
    ('14_15','02-03 PM'),('15_16','03-04 PM'),
    ('16_17','04-05 PM'),('17_18','05-06 PM'),
    ('18_19','06-07 PM'),('19_20','07-08 PM'),
    ('20_21','08-09 PM'),('21_22','09-10 PM'),
    ('22_23','10-11 PM'),('23_24','11-12 PM'),
    ('24_1','12-01 AM'),('1_2','01-02 AM'),
    ('2_3','02-03 AM'),('3_4','03-04 AM'),
    ('4_5','04-05 AM'),('5_6','05-06 AM'),
    ('6_7','06-07 AM'),('7_8','07-08 AM')
]

selection_obj = [
    ('temp','Temp'),('pulse','Pulse'),
    ('rr','RR'),('bp','BP'),
    ('spo2','Spo2'),('unit','Unit'),
    ('sign','Sign with Emp. ID')
]

dec_obj = [
    ('accompanying','a. Accompanying symptoms (e.g. Nausea)'),('sleep','b. Sleep'),
    ('appetite','c. Appetite'),('physical','d. Physical activity'),
    ('relationship','e. Relationship with others (e.g. Irritability)'),('emotions','f. Emotions (e.g. anger,suicidal,crying)'),
    ('concentration','g. Concentration'),('other','h. Other')
]

act_obj = [
    ('feeding','Feeding'),('bathing','Bathing'),
    ('toileting','Toileting'),('general','General mobility/ Gait'),
    ('dressing','Dreesing/Grooming'),
]


family_history_obj = [
    ('hypertension','Hypertension'),('heart_disease','Heart Disease'),
    ('diabetes','Diabetes'),('dyslipidemia','Dyslipidemia'),
    ('asthma','Asthma'),
    ('stroke','Stroke'),
    ('other','Other Chronic Disease'),        
]

class CareplanHmsDetail(models.Model):
    _name = 'careplan.hms.detail'
    _description = 'Care Plan Details'
    _rec_name = 'careplan_hms_id'

    @api.multi
    def button_approve(self):
        self.state = 'approve'

    @api.multi
    def button_done(self):
        self.state = 'done'
        self.user_id = self.env.user

    careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization", states={'done': [('readonly', True)]})
    date_careplan = fields.Datetime('Date', required="True", default=fields.Datetime.now, states={'done': [('readonly', True)]})
    patient_id = fields.Many2one('hms.patient','Patient', states={'done': [('readonly', True)]})
    #day_careplan = fields.Char('Day', readonly="True")
    pod = fields.Char('POD', states={'done': [('readonly', True)]})
    temp = fields.Char('Temperature', states={'done': [('readonly', True)]})
    pulse = fields.Char('Pulse', states={'done': [('readonly', True)]})
    bp = fields.Char('BP', states={'done': [('readonly', True)]})
    spo = fields.Char('SPO2', states={'done': [('readonly', True)]})
    resp = fields.Char('Resp', states={'done': [('readonly', True)]})
    sugar = fields.Char('RBC Sugar', states={'done': [('readonly', True)]})
    insulin = fields.Char('Insulin Units', states={'done': [('readonly', True)]})
    oral = fields.Char('Oral Intake', states={'done': [('readonly', True)]})
    ivfluid = fields.Char('Iv Fluid', states={'done': [('readonly', True)]})
    rtfeed = fields.Char('RT Feed', states={'done': [('readonly', True)]})
    urine = fields.Char('Urine', states={'done': [('readonly', True)]})
    stool = fields.Char('Stool', states={'done': [('readonly', True)]})
    vomit = fields.Char('Vomit', states={'done': [('readonly', True)]})
    drain = fields.Char('Drain', states={'done': [('readonly', True)]})
    dress_soak = fields.Char('Dress Soak', states={'done': [('readonly', True)]})
    dress_change = fields.Char('Dress Change', states={'done': [('readonly', True)]})
    sleep = fields.Char('Sleep', states={'done': [('readonly', True)]})
    bed_soar = fields.Char('Bed Sores', states={'done': [('readonly', True)]})
    sponging = fields.Char('Sponging', states={'done': [('readonly', True)]})
    bed_sheet = fields.Char('Bed Sheet', states={'done': [('readonly', True)]})
    user_id = fields.Many2one('res.users', "Done By", states={'done': [('readonly', True)]})
    check_id = fields.Many2one('res.users', 'Check By', default=lambda self: self.env.user, states={'done': [('readonly', True)]})
    update_id = fields.Many2one('res.users', 'Update By', readonly="True", states={'done': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('approve','Approve'),('done','Done')], 'State', readonly=True, default="draft")


class IndimediCareplan(models.Model):
    _inherit = "inpatient.registration"

    def _get_vitals_io_chart_ids(self):
        result = []
        for time in selection_time:
            result.append((0, 0, {'time': time[0]}))
        return result       


    def _get_obj(self):
        lis = []
        for obj in selection_obj:
            lis.append((0, 0, {'post_ob':obj[0]}))
        return lis


    def _get_dec_obj(self):
        lis = []
        for obj in dec_obj:
            lis.append((0, 0, {'name':obj[0]}))
        return lis

    def _get_obj(self):
        lis = []
        for obj in selection_obj:
            lis.append((0, 0, {'post_ob':obj[0]}))
        return lis


    def _get_dec_obj(self):
        lis = []
        for obj in dec_obj:
            lis.append((0, 0, {'name':obj[0]}))
        return lis

    def _get_act_obj(self):
        activity = []
        for obj in act_obj:
            activity.append((0, 0, {'activity':obj[0]}))
        return activity


    def _get_family_history_obj(self):
       vals = []
       datas = self.env['nusring.family.history'].search([])
       for data in datas:
           vals.append((0, 0, {
               'name': data.name,
               'father': False,
               'mother': False,
               'sister': False,
               'brother': False,
           }))
       return vals

    @api.model
    def _get_past_history_obj(self):
       vals = []
       datas = self.env['nusring.past.history'].search([])
       for data in datas:
           vals.append((0, 0, {
               'name': data.name,
               'value': 'no',
           }))
       return vals

    @api.model
    def _default_vulnerable(self):
       vals = []
       datas = self.env['vulnerable.assessment'].search([])
       for data in datas:
           vals.append((0, 0, {
               'name': data.name,
           }))
       return vals

    # @api.model
    # def _default_preopinvchecklist(self):
    #     vals = []
    #     preopinvchecklists = self.env['preoperative.investigation.template'].search([])
    #     for preopinvchecklists in preopinvchecklists:
    #         vals.append((0,0,{
    #             'name': preopinvchecklists.name,
    #         }))
    #     return vals

    # @api.model
    # def _default_preopinfochecklist(self):
    #     vals = []
    #     preopinfochecklists = self.env['preoperative.information.template'].search([])
    #     for preopinfochecklists in preopinfochecklists:
    #         vals.append((0,0,{
    #             'name': preopinfochecklists.name,
    #         }))
    #     return vals

    careplan_hms_ids = fields.One2many('careplan.hms.detail', 'careplan_hms_id', string="Careplan")

    #ER Assessment Form
    #Mode of Arrival
    #Source
    x_test_range = fields.Integer(string='Range')
    er_date = fields.Datetime('Date & Time',default=fields.Datetime.now)
    walk_in = fields.Boolean(string="Walk in")
    wheelchair = fields.Boolean(string="Wheelchair")
    p_family = fields.Boolean(string="Patient Family")
    friends = fields.Boolean(string="Friends")
    guardian = fields.Boolean(string="Guardian")    
    hospital = fields.Boolean(string="Hospital")
    paramedic = fields.Boolean(string="Paramedic")
    police = fields.Boolean(string="Police")    
    other_source = fields.Boolean(string="Other")    
    #Triage
    life_th_emer = fields.Boolean(string="Life Threating Emergency")
    non_emer = fields.Boolean(string="Non Emergency")
    non_life_th_emer = fields.Boolean(string="Non Life Threating Emergency")
    brought_dead = fields.Boolean(string="Brought Dead")
    #Prehospital
    cpr = fields.Boolean(string="CPR")
    intuba = fields.Boolean(string="Intuba")
    o2 = fields.Boolean(string="O2")
    iv = fields.Boolean(string="IV")
    c_collar = fields.Boolean(string="C-collar")
    splints = fields.Boolean(string="Splints")
    meds = fields.Boolean(string="Meds")
    none = fields.Boolean(string="None")
    #Vital Sings
    temp_er = fields.Char(string="Temp(°F)")
    pulse_er = fields.Char(string="Pulse(/min)")
    rr_er = fields.Char(string="R/R(/min)")
    bp_er = fields.Char(string="BP(mm)")
    spo2_er = fields.Char(string="HgSpo2(%)")
    #Nursing Examination
    #cons
    alert = fields.Boolean(string="Alert")
    appear = fields.Boolean(string="Well-appearing")
    confused = fields.Boolean(string="Confused")
    poor_res = fields.Boolean(string="Poor responsive")
    unconscious = fields.Boolean(string="Unconscious")
    #Respiratory
    rl_bill = fields.Boolean(string="R L Bill")
    wheezer_rates = fields.Boolean(string="Wheezer Rates")
    rhonchile = fields.Boolean(string="Rhonchile")
    normal_res = fields.Boolean(string="Normal")
    #CV
    techycardia = fields.Boolean(string="Techycardia")
    bradycardia = fields.Boolean(string="Bradycardia")
    irregular = fields.Boolean(string="Irregular")
    normal_cv = fields.Boolean(string="Normal")
    #Neurologic Oriented to
    time_neuro = fields.Boolean(string="Time")
    person_neuro = fields.Boolean(string="Person")
    place_neuro = fields.Boolean(string="Place")
    not_oriented = fields.Boolean(string="Not Oriented")
    un_test = fields.Boolean(string="Unable to test")
    normal_neuro = fields.Boolean(string="Normal")
    #Motor Func
    rl_arm = fields.Boolean(string="R L Arm")
    leg = fields.Boolean(string="Leg")
    face = fields.Boolean(string="Face")
    weak = fields.Boolean(string="Weak")
    un_test_func = fields.Boolean(string="Unable to test")
    normal_func = fields.Boolean(string="Normal")
    other_exam = fields.Char(string="Other")
    #Orders,Interventions & Results
    consult_notify = fields.Boolean(string="Consultant notified")
#    glucometer = fields.Char(string="Glucometer (mg/dl)")
    rbs = fields.Char(string="RBS(mg/dl)")
    o2_inter = fields.Char(string="O2")
    iv_inter = fields.Char(string="IV")
    monitor_inter = fields.Char(string="Monitor")
    ecg_inter = fields.Char(string="ECG at (am/pm)")
    cxr = fields.Char(string="CXR")
    labs_inform = fields.Char(string="Labs: Informed To")
    labs_ordered = fields.Char(string="Labs Ordered")
    consulted_by = fields.Many2one('res.users','Collected By', default=lambda self: self.env.user, readonly="1")
    #Table
    treatment_er_department_ids = fields.One2many('treatment.er.department','treatment_er_department_id',string='Treatment Er Department')
    inter_obser_ids = fields.One2many('intervention.observation','careplan_hms_id')
    weight_inter = fields.Float(string="Weight")
    #cond_patient = fields.Selection([('improved','Improved'),('unchanged','Unchanged'),('deteriorate','Deteriorate'),('expired','Expired')],string="Condition of Patient")
    cond_patient_improved = fields.Boolean(string='Improved')
    cond_patient_unchanged = fields.Boolean(string='Unchanged')
    cond_patient_deteriorate = fields.Boolean(string='Deteriorate')
    cond_patient_expired = fields.Boolean(string='Expired')
    transferto_home = fields.Boolean(string="Home")
    transferto_icu = fields.Boolean(string="ICU")
    transferto_ward = fields.Boolean(string="Ward")
    transferto_ot = fields.Boolean(string="OT")
    transferto_other = fields.Boolean(string="Other")
    transferto_other_note = fields.Char(string="Note")
    home = fields.Boolean(string="Home")
    transfer = fields.Boolean(string="Transfer")    
    trans_text = fields.Char(string="Transfer")
    transfer_time = fields.Datetime(string="Transfer Time")
    #Nurses Hand Over Sheet
    morning_ids = fields.One2many('morning.shift','careplan_hms_id')
    evening_ids = fields.One2many('evening.shift','careplan_hms_id')
    night_ids = fields.One2many('night.shift','careplan_hms_id')
    #Nurse:--Discharge Checklist
    unit_name = fields.Char(string="Unit Name")
    ident_band =fields.Boolean(string="Identification band off")
    intra_cath = fields.Boolean(string="Intra cath (I/V) removed")
    urinary_cath = fields.Boolean(string="Urinary catheter removed")
    dis_given_expl = fields.Boolean(string="Discharge summary given & explained to patient")
    home_medication = fields.Boolean(string="Home Medication given & Patient explained the correct dose and frequency of medications")
    wound_dress = fields.Boolean(string="Patient explained about wound dressing needs, if any")
    vuln_safety = fields.Boolean(string="Vulnerable Patient Explained about Safety Measures")
    process_followup = fields.Boolean(string="Patient explained process of follow-up visit and contact numbers")
    emergency_no = fields.Boolean(string="Patient explained on who and how to contact in case of emergency")
    home_care = fields.Boolean(string="Home care explainations given")
    patient_relative = fields.Char(string="Patient / Relative Name")
    dis_check_time = fields.Datetime(string="Date & Time")
    login_username = fields.Many2one('res.users','User', default=lambda self: self.env.user, readonly="1")
    return_demonstration = fields.Boolean(string="Return demonstration")
    verb_understand = fields.Boolean(string="Verbalization of Understanding")
    #Nurse:--Personal Hygiene Chart
    sponge_bath = fields.Boolean(string="Sponge Bath")
    mouth_care = fields.Boolean(string="Mouth Care")
    nail_care = fields.Boolean(string="Nail Care")
    back_care = fields.Boolean(string="Back Care")
    hair_care = fields.Boolean(string="Hair Care")
    bed_sore = fields.Boolean(string="Bed Sore Dressing")
    mouth_gargles = fields.Boolean(string="Mouth Gargles")
    position_changing = fields.Boolean(string="Position Changing")
    eye_care = fields.Boolean(string="Eye Care")
    urine_care = fields.Boolean(string="Urine Catheter Care")
    wound_care = fields.Boolean(string="Wound Dressing Care")
    hygiene_datetime = fields.Datetime(string="Date & Time")
    sponge_obv = fields.Char(string="Observation")
    mouth_obv = fields.Char(string="Observation")
    nail_obv = fields.Char(string="Observation")
    back_obv = fields.Char(string="Observation")
    hair_obv = fields.Char(string="Observation")
    bed_obv = fields.Char(string="Observation")
    mouth_obv = fields.Char(string="Observation")
    position_obv = fields.Char(string="Observation")
    eye_obv = fields.Char(string="Observation")
    urine_obv = fields.Char(string="Observation")
    wound_obv = fields.Char(string="Observation")
    filled_by = fields.Many2one('res.users','Filled by', default=lambda self: self.env.user, readonly="1")
    #Nurse:--Service Provided To Patient
    service_provider_ids = fields.One2many('service.provided','careplan_hms_id')
    #Nurse:---Master Chart
    master_chart_ids = fields.One2many('master.chart','careplan_hms_id', string="Master Chart")
    # #Nurse:---Pre Operative Checklist
    # pre_op_datetime = fields.Datetime(string="Date & Time of Surgery")
    # surgeon_id = fields.Many2one('hms.physician', string="Surgeon")
    # anesthetist_id = fields.Many2one('hms.physician', string="Anesthetist")
    # high_risk = fields.Boolean(string="High Risk")
    # hiv_positive = fields.Boolean(string="HIV Positive")
    # hbsag_preop = fields.Boolean(string="HBsAg")
    # allergy_preop = fields.Char(string="Allergy")
    # pulse_preop = fields.Float(string="Pulse")
    # temp_preop = fields.Float(string="Temp")
    # rr_preop  = fields.Float(string="RR")
    # bp_preop = fields.Float(string="BP")
    # spo2_preop = fields.Float(string="Spo2")
    # rbs_preop = fields.Float(string="RBS")
    # hb_preop = fields.Float(string="HB")
    # blood_group_preop = fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')], string='Blood Group')
    # investigation_preop_ids = fields.One2many('preoperative.investigation','careplan_hms_id', string="Investigation", default=lambda self: self._default_preopinvchecklist())
    # information_preop_ids = fields.One2many('preoperative.information','careplan_hms_id', string="Information", default=lambda self: self._default_preopinfochecklist())
    # ward_nurse_id = fields.Many2one('res.users', ondelete="cascade", string='Ward Nurse', domain=[('is_nurse','=',True)])
    # preop_nurse_id = fields.Many2one('res.users', ondelete="cascade", string='Pre-Op Nurse',domain=[('is_nurse','=',True)])
    # ot_nurse_id = fields.Many2one('res.users', ondelete="cascade", string='OT Nurse', domain=[('is_nurse','=',True)])
    #VITALS I/O CHART
    patient_id1 = fields.Many2one('hms.patient', string="Patient")
    parent_id = fields.Many2one('inpatient.registration', string="Past Record")
    vitals_chart_date = fields.Datetime('Date',default=fields.Datetime.now)
    vitals_io_chart_ids = fields.One2many('vitals.io.chart','careplan_hms_id',string='VITALS I/O Chart',default=lambda self: self._get_vitals_io_chart_ids())
    in_oral = fields.Float('Oral',compute='_get_vitals_total',track_visibility='onchange',store=False)
    in_rtf = fields.Float('NG/RTF/JFT',compute='_get_vitals_total',track_visibility='onchange',store=False)
    in_iv1 = fields.Float('IV1',compute='_get_vitals_total',track_visibility='onchange',store=False)
    in_iv2 = fields.Float('IV2',compute='_get_vitals_total',track_visibility='onchange',store=False)
    in_tpn = fields.Float('TPN',compute='_get_vitals_total',track_visibility='onchange',store=False)
    ot_rta = fields.Float('RTA',compute='_get_vitals_total',track_visibility='onchange',store=False)
    ot_urine = fields.Float('Urine',compute='_get_vitals_total',track_visibility='onchange',store=False)
    ot_vomit = fields.Float('Vomit',compute='_get_vitals_total',track_visibility='onchange',store=False)
    ot_stool = fields.Float('Stool',compute='_get_vitals_total',track_visibility='onchange',store=False)
    ot_icd1 = fields.Float('ICD1',compute='_get_vitals_total',track_visibility='onchange',store=False)
    ot_icd2 = fields.Float('ICD2',compute='_get_vitals_total',track_visibility='onchange',store=False)
    
    #intra & post operative nursing form

    name_surgery = fields.Many2many('hms_surgery','intra_post_surgery_names','post_id','surgery_id', ondelete="restrict", string='Name of Surgery/Procedure')
    type_of_anesthesia = fields.Many2one('res.users','Type of Anesthesia given')
    intra_operative1 = fields.Char(string="1.")
    intra_operative2 = fields.Char(string="2.")
    intra_operative3 = fields.Char(string="3.")
    intra_operative4 = fields.Char(string="4.")
    drainage_rlt = fields.Selection([('rt','Rt'),('lt','Lt')],string='Intercositals Drainage')
    drain_rlt = fields.Selection([('rt','Rt'),('lt','Lt')],string='Drain')
    epidural_yn = fields.Selection([('yes','Yes'),('no','No')],string='Epidural Catheter')
    cvp_line = fields.Char(string="CVP Line")
    biopsy_sent = fields.Selection([('yes','Yes'),('no','No')], string="Biopsy sent:")
    specimen = fields.Char(string="Specimen")
    name_laboratory = fields.Char(string="Name of Laboratory")
    intra_post_sent_by = fields.Char(string="Sent By")
    intra_post_time = fields.Char(string="Time")
    specific_position_surgery = fields.Char(string="Surgery")
    intra_post_rbs = fields.Char(string="RBS(Hourly)")
    medication_detail_ids = fields.One2many('medications.detail','medication_detail_id',string='Post Operative Medication')
    icu_ids = fields.One2many('post.operation','staff',string="To be filled by post Operative", default=lambda self:self._get_obj())
    ot_nurse = fields.Char(string="OT Nurse")
    post_nurse = fields.Char(string="Post Of Nurse")
    ward_nurse = fields.Char(string="Ward Nurse")
    emp_id_ot = fields.Char(string="Sign with Emp.ID")
    emp_id_post = fields.Char(string="Sign with Emp.ID")
    emp_id_ward = fields.Char(string="Sign with Emp.ID")
    ot_to_ward_time = fields.Char(string="Time")
    post_to_ward_time = fields.Char(string="Time")
    ward_to_ward_time = fields.Char(string="Time")

    #pain rating assessment sheet

    pain_constant = fields.Selection([('yes','Yes'),('no','No')])
    front = fields.Selection([('right','Right'),('left','Left')],string="Front")
    left_side = fields.Selection([('right','Right'),('left','Left')],string="Left Side")
    back = fields.Selection([('right','Right'),('left','Left')],string="Back")
    right_side = fields.Selection([('right','Right'),('left','Left')],string="Right Side")
    neck = fields.Selection([('right','Right'),('left','Left')],string="Neck")
    face = fields.Selection([('right','Right'),('left','Left')],string="Face")
    legs = fields.Selection([('right','Right'),('left','Left')],string="Legs")
    ancle = fields.Selection([('right','Right'),('left','Left')],string="Ancle")

    occur = fields.Char(string="occur")
    increase_pain = fields.Char(string="Increase Pain")
    pain_question = fields.Char(string="Pain Question")
    effect_of_pain_ids = fields.One2many('effect.pain','effect_id', string="effect", default=lambda self:self._get_dec_obj())
    pain_relieve = fields.Boolean(string="a. Pain relieving drugs")
    hot_and_cold_packs = fields.Boolean(strings="packs")
    changing_position = fields.Boolean(string="Changing position")
    exercise_or_physiotherapy = fields.Boolean(string="Physiotherapy")
    massage = fields.Boolean(string="Massage")
    psychological = fields.Boolean(string="Psychological")
    prayer_meditation = fields.Boolean(string="Prayer Meditation")
    relaxation_teq = fields.Boolean(string="Relaxation teq.")
    creative_teq = fields.Boolean(string="creative teq.")
    other_teq = fields.Char(string="other teq.")
    patient_relative = fields.Char(string="Patient relative" )
    ache_pain = fields.Selection([
        ('ache','Ache'),('deep','Deep'),
        ('sharp','Sharp'),('Hot','hot'),
        ('cold','Cold'),('itchy_ect','Itchy ect')],string="Characteristics of Pain")
    intensity_pain = fields.Selection([
        ('no_hurt','No Hurt'),('hurts_little_bit','Hurts Little Bit'),
        ('hurts_little_more','Hurts Little More'),('hurts_even_more','Hurts Even More'),
        ('hurts_whole_lot','Hurts Whole Lot'),('hurts_worst','Hurts Worst')],string="Intensity Pain")
    pain_medicine = fields.One2many('pain.control','non_drug', string="medicine of pain")

    # nursing admission assessment form
     
    initial_date = fields.Date('Date',)
    initial_unit = fields.Char('Unit')
    arrival_time = fields.Char('Patient Arrival time:')
    patient_height = fields.Char('Height')
    patient_weight = fields.Char('Weight')
    ht_wt = fields.Char('ht/wt')
    history = fields.Char('history')
    relationship = fields.Char('Relationship')
    patient_arrival = fields.Selection([
        ('ambulatory','Ambulatory'),('wheelchair','Wheelchair'),
        ('stretcher','Stretcher'),('other','Other')
        ],string='Patient Arrival')
    patient_arrival_from = fields.Selection([
        ('home','Home'),('opd','OPD'),
        ('other','Other')],string='Patient Arrival From')
    id_band = fields.Selection([('yes','Yes'),('no','No')])
    call_bell = fields.Selection([('yes','Yes'),('no','No')])
    temp = fields.Char('Temperature(°F)')
    v_pulse = fields.Char('Pulse(/min)')
    v_rr = fields.Char('RR(/min)')
    blood_pressure = fields.Char('Blood Pressure(mm)')
    hgspo2 = fields.Char('HgSpO2(%)')
    denture = fields.Selection([('yes','Yes'),('no','No')],string='Denture')
    eye_aid = fields.Selection([('yes','Yes'),('no','No')],string='Eye aid')
    upper = fields.Boolean('Upper')
    lower = fields.Boolean('Lower')
    partial = fields.Boolean('Partial')
    glasses = fields.Boolean('Glasses')
    contacts = fields.Boolean('Contacts')
    none = fields.Boolean('None')
    other_ad = fields.Boolean('Other')
    other_ad_note = fields.Char('Other_1')
    chief_complaint = fields.Text('Cheif Complaint')
    diagnosis = fields.Text('Diagnosis')
    allergies = fields.Selection([('yes','Yes'),('no','No')],'Allergy')
    drug = fields.Boolean('Drug')
    food = fields.Boolean('Food')
    other_all = fields.Boolean('Other')
    blood_tranfusion = fields.Selection([('yes','Yes'),('no','No')],'Reaction previous Blood transfusion')
    decs = fields.Char('If yes,descibe')
    alert = fields.Boolean('Alert')
    lethargic = fields.Boolean('Lethargic')
    responsive_pain = fields.Boolean('Responsive to pain')
    unresponsive_pain = fields.Boolean('unresponsive to Pain')
    walker = fields.Boolean('Walker')
    cane = fields.Boolean('Cane')
    crutched = fields.Boolean('Crutched')
    other_device = fields.Boolean('Other')
    other_1 = fields.Char('Other_1')
    name_nursing_staff = fields.Char('Name of Nursing staff')
    date_1 = fields.Date('Date')
    time_1 = fields.Char('Time')
    
    f_hypertension = fields.Selection([('yes','Yes'),('no','No')], 'Hypertension')
    f_heart_disease = fields.Selection([('yes','Yes'),('no','No')], 'Heart Disease')
    f_diabetes = fields.Selection([('yes','Yes'),('no','No')], 'Diabetes')
    f_dyslipidemia = fields.Selection([('yes','Yes'),('no','No')], 'Dyslipidemia')
    f_asthma = fields.Selection([('yes','Yes'),('no','No')], 'Asthma')
    f_stroke = fields.Selection([('yes','Yes'),('no','No')],'Stroke')
    f_cancer = fields.Selection([('yes','Yes'),('no','No')],'Cancer')
    f_other_chronic = fields.Selection([('yes','Yes'),('no','No')],'Other Chronic Disease')
    
    family_history_ids = fields.One2many('nusring.family.history','nursing_family_history_id',string='Family History',default=lambda self:self._get_family_history_obj())
    past_history_ids = fields.One2many('nusring.past.history','nursing_past_history_id',string='Past History',default=lambda self:self._get_past_history_obj())

    pa_hypertension = fields.Selection([('yes','Yes'),('no','No')], 'Hypertension')
    pa_heart_disease = fields.Selection([('yes','Yes'),('no','No')], 'Heart Disease')
    pa_diabetes = fields.Selection([('yes','Yes'),('no','No')], 'Diabetes')
    pa_dyslipidemia = fields.Selection([('yes','Yes'),('no','No')], 'Dyslipidemia')
    pa_asthma = fields.Selection([('yes','Yes'),('no','No')], 'Asthma')
    pa_stroke = fields.Selection([('yes','Yes'),('no','No')],'Stroke')
    pa_cancer = fields.Selection([('yes','Yes'),('no','No')],'Cancer')
    pa_other_chronic = fields.Selection([('yes','Yes'),('no','No')],'Other Chronic Disease')
    major_surgery = fields.Many2many('hms_surgery','patient_admission_surgery_names','admission_id','surgery_id', ondelete="restrict", string='Surgery')
    surgery_date = fields.Date('Date of Surgery')
    p_diet_formula = fields.Selection([('yes','Yes'),('no','No')],'Diet Formula')
    p_bottle_fed = fields.Selection([('yes','Yes'),('no','No')],'Bottle Fed')
    p_diapers = fields.Selection([('yes','Yes'),('no','No')],'Diapers')
    p_bf = fields.Selection([('yes','Yes'),('no','No')],'BF')
    p_toilet_training = fields.Selection([('yes','Yes'),('no','No')],'Toilet Training')
    p_as_per_schedules = fields.Selection([('yes','Yes'),('no','No')],'schedules')
    p_head_circum = fields.Char('Head circum')
    p_chest_circum = fields.Char('Chest circum')
    r_cough = fields.Boolean('Cough')
    r_asthma = fields.Boolean('Asthma')
    r_dyspnea = fields.Boolean('Dyspnea')
    r_shortness_breath = fields.Boolean('Shortness of Breath')
    r_emphysema = fields.Boolean('Emphysema')
    r_copd = fields.Boolean('COPD')
    r_nad_other = fields.Boolean('NAD Other')
    r_cany_other = fields.Boolean('Any Other')
    nad_other = fields.Char('NAD other')
    any_other = fields.Char('Any other')
    s_intra = fields.Boolean('Intact')
    s_dusky = fields.Boolean('Dusky')
    s_diaphoretic = fields.Boolean('Diaphoretic')
    s_cyanotic = fields.Boolean('Cyanotic')
    s_warm = fields.Boolean('Warm')
    s_pale = fields.Boolean('Pale')
    s_dry = fields.Boolean('Dry')
    s_mattled = fields.Boolean('Mattled')
    s_flushed = fields.Boolean('Flushed')
    s_moist_other = fields.Boolean('Moist Other')
    moist_other = fields.Char('Moist other')
    c_social = fields.Selection([('yes','Yes'),('no','No')],'Social')
    c_lang = fields.Selection([('yes','Yes'),('no','No')],'Language')
    c_phy = fields.Selection([('yes','Yes'),('no','No')],'Physical')
    c_intell = fields.Selection([('yes','Yes'),('no','No')],'Intellectual')
    c_emo = fields.Selection([('yes','Yes'),('no','No')],'Emo')
    c_behavior = fields.Selection([('yes','Yes'),('no','No')],'Behavior')
    specific_remark = fields.Text('Any Specific Remark:')
    c_dizziness = fields.Boolean('Dizziness')
    c_aphasia = fields.Boolean('Aphasia')
    c_headache = fields.Boolean('Headache')
    c_speech = fields.Boolean('Speech')
    c_paralysis = fields.Boolean('Paralysis')
    c_sedation = fields.Boolean('Sedation')
    c_ataxia = fields.Boolean('Ataxia')
    c_slurred = fields.Boolean('Slurred')
    c_nad = fields.Boolean('NAD')
    c_other = fields.Boolean('Other')
    g_pregnant = fields.Boolean('Pregnant')
    g_amenorrhea = fields.Boolean('Amenorrhea')
    g_venereal = fields.Boolean('Venereal')
    g_urinary_incotinence = fields.Boolean('Urinary Incotinence')
    g_retention = fields.Boolean('Retention')
    g_having_menses = fields.Boolean('Having Menses')
    g_dysmenorrhea = fields.Boolean('Dysmenorrhea')
    g_hematuria = fields.Boolean('Hematuria')
    g_dysuria = fields.Boolean('Dysuria')
    g_disease = fields.Boolean('Disease')
    g_enuresis = fields.Boolean('Enuresis')
    g_other = fields.Boolean('Other')
    g_nad = fields.Boolean('NAD')
    ga_vomiting = fields.Boolean('Vomiting')
    ga_nausea = fields.Boolean('Nausea')
    ga_ulcer = fields.Boolean('Ulcer')
    ga_constipation = fields.Boolean('Constipation')
    ga_blood_stool = fields.Boolean('Blood in stool')
    ga_diarrhea = fields.Boolean('Diarrhea')
    ga_hepatitis = fields.Boolean('Hepatitis')
    ga_nad = fields.Boolean('NAD')
    ga_other = fields.Boolean('Other')
    ga_other_c = fields.Char('Other')
    c_angina = fields.Boolean('Angina')
    c_peripheral = fields.Boolean('Peripheral')
    c_htn = fields.Boolean('HTN')
    c_pacemaker = fields.Boolean('Pacemaker')
    c_heart_murmur = fields.Boolean('Heart murmur')
    c_sob = fields.Boolean('SOB')
    c_chest_pain = fields.Boolean('Chest Pain')
    c_edema = fields.Boolean('Edema')
    c_hx_mi = fields.Boolean('Hx MI')
    c_nad = fields.Boolean('NAD')
    m_fracture = fields.Boolean('Fracture')
    m_joint = fields.Boolean('Joint Swelling')
    m_muscle_spasm =fields.Boolean('Muscle Spasm')
    m_back_pain = fields.Boolean('Back Pain')
    m_joint_pain = fields.Boolean('Joint Pain')
    m_amputation = fields.Boolean('Amputation')
    m_joint_stiffness = fields.Boolean('Joint Stiffness')
    m_nad = fields.Boolean('NAD')

    o_hyperthyroid = fields.Boolean('Hyperthyroid Diabetes')
    o_hiv_aids = fields.Boolean('HIV AIDS')
    o_hepatitis = fields.Boolean('Hepatitis')
    c_hepatitis = fields.Char('(Specify)')
    o_other = fields.Boolean('Other(Specify)')
    o_other_note = fields.Char('Specify(Note)')

    activity_daily_living_ids = fields.One2many('daily.living','a_daily_living','Activity Of Daily Living',default=lambda self:self._get_act_obj())
    vulnerable_assessment_ids = fields.One2many('vulnerable.assessment','cat_id','Vulnerable assessment',default=lambda self:self._default_vulnerable())
    high_vulnerability = fields.Boolean(string='High Vulnerability')
    low_vulnerability = fields.Boolean(string='Low Vulnerability')
    pain_assessment = fields.Selection([('yes','Yes'),('no','No')],'Pain assessment')
    pain_location = fields.Char('Pain Location')
    quality = fields.Selection([('constant','Constant'),('intermittent','Intermittent')],'Quality')
    character = fields.Selection([('lacerating','Lacerating'),('burning','Burning'),('radiating','Radiating')],'Character')
    after_daily_routine = fields.Selection([('yes','Yes'),('no','No')],'After daily routine')
    sleep_s = fields.Selection([('yes','Yes'),('no','No')],'Sleep') 
    pain_scale = fields.Selection([
            ('no_hurt','No Hurt'),('hurts_little','Hurts Little Bit'),
            ('hurt_little_more','Hurt Littel More'),('hurts_even_more','Hurts Even More'),
            ('hurts_whole_lot','Hurts Whole Lot'),('hurts_worst','Hurts Worst')],'Pain Rating Scale')
    pain_scale_value = fields.Integer(string='Value')
    
    #Burden Scale
    sensory_percep_value = fields.Selection([
        ('no_impairment', 'No Impairment'),
        ('slightly_limited', 'Slightly Limited'),
        ('very_limited', 'Very Limited'),
        ('completely_limited', 'Completely Limited'),
    ], string='Sensory Percep', default = 'no_impairment')
    sensory_percep_score = fields.Integer('Score')
    moisture_value = fields.Selection([
        ('rarely_moist','Rarely Moist'),
        ('occasionally_moist', 'Occasionally Moist'),
        ('very_moist', 'Very Moist'),
        ('constantly_moist', 'Constantly Moist'),
    ], string='Moisture',default = 'rarely_moist')
    moisture_score = fields.Integer('Score')
    degreeofac_value = fields.Selection([
        ('walks_frequently','Walks Frequently'),
        ('walks_occasionally','Walks Occasionally'),
        ('chair_fast', 'Chair Fast'),
        ('bed_fast', 'Bed Fast')],default = 'walks_frequently',string='Degree of AC')
    degreeofac_score = fields.Integer('Score')
    mobility_value = fields.Selection([
        ('no_impairment', 'No Impairment'),
        ('slightly_limited', 'Slightly Limited'),
        ('very_limited', 'Very Limited'),
        ('completely_limited', 'Completely Limited'),
    ], string='Mobility', default = 'no_impairment')
    mobility_score = fields.Integer('Score')
    nutrition_value = fields.Selection([
        ('excellent','Excellent'),
        ('adequate', 'Adequate'),
        ('in_adequate', 'In-adequate'),
        ('very_poor', 'Very Poor'),
    ], string='Nutrition',default = 'excellent')
    nutrition_score = fields.Integer('Score')
    shear_friction_value = fields.Selection([
        ('no_problem','No Problem'),
        ('potential_problem','Potential Problem'),
        ('problem_present', 'Problem Present')],default = 'no_problem',string='Shear & Friction')
    shear_friction_score = fields.Integer('Score')
    burden_scale_final_total = fields.Integer('Burden Scale Total Score',compute='_burden_scale_total')
    pressure_sore = fields.Char('pressure sore')


    #Fall Risk Assessment
    history_fall_value = fields.Selection([      
        ('history_fall', 'History Fall'),
    ], string='History Fall', default = 'history_fall')
    history_fall_score = fields.Integer('Score')

    physical_status_value = fields.Selection([
        ('ataxia','Fa(Friedreich"s ataxia)'),
        ('dizziness', 'Dizziness/Balance Problems'),
        ('impaired', 'Impaired Mobility'),
        ('sensory', 'Sensory Impairment'),
        ('seizure', 'Seizure Disorder'),
        ('altera', 'Altera'),
    ], string='Physical Status',default = 'ataxia')
    physical_status_score = fields.Integer('Score')

    mental_status_value = fields.Selection([
        ('confused','Confused(illogical thinking)'),
        ('impaired','Impaired Memory/Judgement'),
        ('disoriented', 'Disoriented to Person/Place/Time'),
        ('familiarity', 'Lack of familiarity  with immediate surroundings'),
        ('inability', 'Inability to understand/follow instuction'),
        ],default = 'confused',string='Mental Status')
    mental_status_score = fields.Integer('Score')

    medication_status_value = fields.Selection([
        ('medication_drugs','Drugs that have diuretic effect'),
        ('medication_effect','Drugs that alter throughout process and/or create hypotensive effect(narcotic, sedatives, psychotropic, hyponotic traquilizers, Anti-Hypertensive)'),
        ('medication_gimo', 'Drugs that increase GI mo (Laxatives, Enemas, Chathartics)'),
        ('medication_multiple_drugs', 'Multiple drugs from different drug classifications'),
        ],default = 'medication_drugs',string='Medication')
    medication_status_score = fields.Integer('Score')
    fall_risk_final_total = fields.Integer('Fall Risk Total Score',compute='_fall_risk_final_total')
    msg = fields.Char('Potential Risk for falls')
    msg1 = fields.Char('Note:')

    #GSC
    eye_value = fields.Selection([
        ('no_response', 'No Response'),
        ('to_pain', 'To Pain'),
        ('to_speech', 'To Speech'),
        ('spotaneously', 'Spotaneously'),
    ],default='spotaneously',string='Eye Opening')
    eye_score = fields.Integer('Score')
    best_verbal_value = fields.Selection([
        ('no_response','No Verbal Response'),
        ('incomprehensible_sounds', 'Response within Comprehensible Sounds'),
        ('inappropriated_words', 'Inappropriate Words in Comprehensible'),
        ('confused', 'Confused'),
        ('oriented_time_person', 'Oriented'),
    ],default='oriented_time_person',string='Best Verbal Response')
    best_verbal_score = fields.Integer('Score')
    best_motor_value = fields.Selection([
        ('no_response','No Response'),
        ('abnormal_extension','Extension'),
        ('abnornal_flexion', 'Flexion-Abnormal'),
        ('flexion_drawal', 'Flexion-Withdrawal'),
        ('moves_localized', 'Localized Pain'),
        ('obeys_commands', 'Obeys a Siple Response')] ,default='obeys_commands', string='Best Motor Response')
    best_motor_score = fields.Integer('Score')
    gcs_final_total = fields.Integer('GCS Total Score',compute='_gcs_total')
    gcs_na = fields.Boolean('NA',default=False,compute='_gcs_total')
    history_medicatiion_ids = fields.One2many('history.medication','history_medicatiion','History Medication')
    g_sponging = fields.Boolean('Sponging/enema')
    g_mouth = fields.Boolean('Mouth care/mouth Gargles')
    g_nail = fields.Boolean('Nail care')
    g_back = fields.Boolean('Back care')
    g_vitals = fields.Boolean('Vitals')
    g_drain = fields.Boolean('Drain')
    g_dressing = fields.Boolean('Dressing')
    g_phycological_support = fields.Boolean('Phycological support')

    c_fluid = fields.Boolean('IV fluid')
    c_antibiotic = fields.Boolean('Antibiotic')
    c_causative = fields.Boolean('Causative treatment')
    c_Continue = fields.Boolean('Continue Previous Medication')
    c_self_medica = fields.Boolean('Self medica')
    c_high_risk = fields.Boolean('High risk medication')

    d_oral_drug = fields.Boolean('Oral drug')
    d_insulin = fields.Boolean('Insulin plan')

    n_ryle = fields.Boolean('Ryle tube feeding')
    n_parental = fields.Boolean('Parental nutrition')
    n_food = fields.Boolean('Type of Food')
    n_type = fields.Char('n Type')

    physiotherapy_need = fields.Selection([('yes','Yes'),('no','No')],'Physiotherapy Need')
    pain_management = fields.Selection([('yes','Yes'),('no','No')],'Pain Management')
    relieving_factor = fields.Boolean('Reliving factor')
    rest = fields.Boolean('Rest')
    Medication_b = fields.Boolean('Medication')
    other_b = fields.Boolean('Other')

    s_side = fields.Boolean('Side rail provision')
    s_low_bed = fields.Boolean('Low bed height')
    s_near = fields.Boolean('Near to nursing station')
    s_continue = fields.Boolean('Continues monitoring')
    s_light = fields.Boolean('Light & sound monitoring')
    s_lang = fields.Boolean('Language translator required')
    s_full_time = fields.Boolean('Full time attendant')
    blood_tranfusion_s = fields.Selection([('yes','Yes'),('no','No')],default='no',string='Blood transfusion')
    approx_req = fields.Char('Approx requirement inf formed by doctor:')
    specific_equ = fields.Selection([('yes','Yes'),('no','No')],default='no',string='Any specific equipment')
    if_yes = fields.Char('Note')
    any_procedure = fields.Char('Any procedure')
    b_positioning = fields.Boolean('Positioning Changing')
    b_bedsore = fields.Boolean('Bedsore dressing')
    b_education = fields.Boolean('Education to patient/relative')
    b_application = fields.Boolean('Application of cream')
    i_regular = fields.Boolean('Regular monitoring of site')
    i_washing = fields.Boolean('Hand washing')
    specific_remark_2 = fields.Text('Any Specific Remark:')
    name_patient = fields.Char('Name of Patient/Relative:')
    name_staff = fields.Many2one('res.users','Name of Nursing staff:', default=lambda self: self.env.user, readonly="1")
    date_2 = fields.Datetime('Date-time')
    nursing_master_chart_ids = fields.One2many('nursing.io.chart', 'nursing_chart_ids', string="Nursing Master Chart")
    sbar_shift = fields.Char(string='Shift')
    sbar_datetime = fields.Datetime(string='Datetime',default=fields.Date.context_today)
    sbar_note = fields.Text(string='Nurses note:')
    sbar_patient = fields.Text(string='Patient and family education')
    sbar_diagnosis = fields.Text(string='Admitting diagnosis/Secondary diagnosis:')
    sbar_isolation = fields.Text(string='Infected/Non Infected/Isolation')
    sbar_iv = fields.Char(string="I/V Line:")
    sbar_date_of_insertion = fields.Date(string="Date of Insertion:",default=fields.Date.context_today)
    sbar_cvc_line = fields.Char(string="CVC Line")
    sbar_cvc_insertion = fields.Date(string="Date of Insertion:",default=fields.Date.context_today)
    sbar_issues = fields.Text(string='Most current issues')
    sbar_foleys_insertion = fields.Date(string="Date of Foley's insertion",default=fields.Date.context_today)
    sbar_rt_date = fields.Date(string="Date of RT/NJ/FJ",default=fields.Date.context_today)
    sbar_procedure = fields.Text(string="Any procedure/surgery done:")
    sbar_wounds = fields.Text(string="Wounds/Dressing")
    sbar_recent = fields.Text(string="Recent Intervention:")
    sbar_status = fields.Char(string="Bedsore status, stage")
    sbar_location = fields.Char(string="Location")
    sbar_treatment = fields.Char(string="Treatment")
    discharge_planning_transfer = fields.Text(string='Discharge Planning')
    sbar_pre = fields.Text(string="Pre & post-operative instruction, if any")
    sbar_nursing_care = fields.Text(string="Nursing Care Plan for next shift:")
    sbar_care_issues = fields.Text(string="Care issues requiring follow-up:")
    sbar_pending = fields.Text(string="Pending treatment/investigation")
    sbar_sign = fields.Char(string="Sign. of over given by:(with EID)")
    sbar_sign_taken  = fields.Char(string="Sign of over taken by:(with EID)")


    # @api.onchange('vulnerable_assessment_ids')
    # def onchange_assessment_ids(self):
    #     data = self.vulnerable_assessment_ids.mapped('yes')
    #     if data.count('True') > 1:
    #         self.high_vulnerability == True
    #     if data.count('True') == 1:
    #         self.low_vulnerability == True
    

    @api.onchange('vitals_chart_date')
    def onchange_vitals_chart_date(self):
        if self.vitals_chart_date:
            date_time = (datetime.strptime(self.vitals_chart_date, DT)-timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
            date_time2 = (datetime.strptime(self.vitals_chart_date, DT)-timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')
            domain = [('patient_id1', '=', self.patient_id1.id), 
                ('vitals_chart_date', '>=', date_time),
                ('vitals_chart_date', '<=', date_time2),
                ]
            self.parent_id = self.search(domain, limit=1).id
            # return {'domain': {'parent_id': domain}}

    @api.depends('vitals_io_chart_ids')
    def _get_vitals_total(self):
            for vitals in self:
                for line in vitals.parent_id.vitals_io_chart_ids:
                    vitals.in_oral += line.vitals_oral
                    vitals.in_rtf += line.vitals_ng_rtf_jft
                    vitals.in_iv1 += line.vitals_iv1
                    vitals.in_iv2 += line.vitals_iv2
                    vitals.in_tpn += line.vitals_tpn
                    vitals.ot_rta += line.vitals_rta
                    vitals.ot_urine += line.vitals_urine
                    vitals.ot_vomit += line.vitals_vomit
                    vitals.ot_icd1 += line.vitals_icd1
                    vitals.ot_icd2 += line.vitals_icd2


    @api.onchange('sensory_percep_value')
    def onchange_sensory_percep_value(self):
        if self.sensory_percep_value == "no_impairment":
            self.sensory_percep_score = '4'
        if self.sensory_percep_value == "slightly_limited":
            self.sensory_percep_score = '3'
        if self.sensory_percep_value == "very_limited":
            self.sensory_percep_score = '2'
        if self.sensory_percep_value == "completely_limited":
            self.sensory_percep_score = '1'


    @api.onchange('moisture_value')
    def onchange_moisture_value(self):
        if self.moisture_value == "rarely_moist":
            self.moisture_score = '4'
        if self.moisture_value == "occasionally_moist":
            self.moisture_score = '3'
        if self.moisture_value == "very_moist":
            self.moisture_score = '2'
        if self.moisture_value == "constantly_moist":
            self.moisture_score = '1'


    @api.onchange('degreeofac_value')
    def onchange_degreeofac_value(self):
        if self.degreeofac_value == "walks_frequently":
            self.degreeofac_score = '4'
        if self.degreeofac_value == "walks_occasionally":
            self.degreeofac_score = '3'
        if self.degreeofac_value == "chair_fast":
            self.degreeofac_score = '2'
        if self.degreeofac_value == "bed_fast":
            self.degreeofac_score = '1'


    @api.onchange('mobility_value')
    def onchange_mobility_value(self):
        if self.mobility_value == "no_impairment":
            self.mobility_score = '4'
        if self.mobility_value == "slightly_limited":
            self.mobility_score = '3'
        if self.mobility_value == "very_limited":
            self.mobility_score = '2'
        if self.mobility_value == "completely_limited":
            self.mobility_score = '1'


    @api.onchange('nutrition_value')
    def onchange_nutrition_value(self):
        if self.nutrition_value == "excellent":
            self.nutrition_score = '4'
        if self.nutrition_value == "adequate":
            self.nutrition_score = '3'
        if self.nutrition_value == "in_adequate":
            self.nutrition_score = '2'
        if self.nutrition_value == "very_poor":
            self.nutrition_score = '1'

    @api.onchange('shear_friction_value')
    def onchange_shear_friction_value(self):       
        if self.shear_friction_value == "no_problem":
            self.shear_friction_score = '3'
        if self.shear_friction_value == "potential_problem":
            self.shear_friction_score = '2'
        if self.shear_friction_value == "problem_present":
            self.shear_friction_score = '1'

    @api.depends('sensory_percep_score','moisture_score','degreeofac_score','mobility_score','nutrition_score','shear_friction_score')
    def _burden_scale_total(self):
        self.burden_scale_final_total = self.sensory_percep_score + self.degreeofac_score + self.mobility_score + self.nutrition_score + self.nutrition_score + self.shear_friction_score
            
    @api.onchange('burden_scale_final_total')
    def onchange_burden_scale_final_total(self):
        if self.burden_scale_final_total <= 9:
            self.msg1 = _('Severe Risk')
        if self.burden_scale_final_total >= 10 and self.burden_scale_final_total <= 12:
            self.msg1 = _('High Risk')
        if self.burden_scale_final_total >= 13 and self.burden_scale_final_total <= 14:
            self.msg1 = _('Moderate Risk')
        if self.burden_scale_final_total >= 15 and self.burden_scale_final_total <= 18:
            self.msg1 = _('Mild Risk')
        if self.burden_scale_final_total >= 19 and self.burden_scale_final_total <= 23:
            self.msg1 = _('No Risk')

    @api.onchange('pain_scale')
    def onchange_pain_scale(self):
        if self.pain_scale == "no_hurt":
            self.pain_scale_value = '0'
        if self.pain_scale == "hurts_little":
            self.pain_scale_value = '2'
        if self.pain_scale == "hurt_little_more":
            self.pain_scale_value = '4'
        if self.pain_scale == "hurts_even_more":
            self.pain_scale_value = '6'
        if self.pain_scale == "hurts_whole_lot":
            self.pain_scale_value = '8'
        if self.pain_scale == "hurts_worst":
            self.pain_scale_value = '10'

    @api.onchange('history_fall_value')
    def onchange_history_fall_value(self):
            if self.history_fall_value == "history_fall":
                self.history_fall_score = '2'

                
    @api.onchange('physical_status_value')
    def onchange_physical_status_value(self):
            if self.physical_status_value == "ataxia":
                self.physical_status_score = '2'
            if self.physical_status_value == "dizziness":
                self.physical_status_score = '1'
            if self.physical_status_value == "impaired":
                self.physical_status_score = '1'
            if self.physical_status_value == "sensory":
                self.physical_status_score = '1'
            if self.physical_status_value == "seizure":
                self.physical_status_score = '1'
            if self.physical_status_value == "altera":
                self.physical_status_score = '1'

    @api.onchange('mental_status_value')
    def onchange_mental_status_value(self):
            if self.mental_status_value == "confused":
                self.mental_status_score = '2'
            if self.mental_status_value == "impaired":
                self.mental_status_score = '2'
            if self.mental_status_value == "disoriented":
                self.mental_status_score = '2'
            if self.mental_status_value == "familiarity":
                self.mental_status_score = '1'
            if self.mental_status_value == "inability":
                self.mental_status_score = '1'

    @api.onchange('medication_status_value')
    def onchange_medication_status_value(self):
            if self.medication_status_value == "medication_drugs":
                self.medication_status_score = '1'
            if self.medication_status_value == "medication_effect":
                self.medication_status_score = '1'
            if self.medication_status_value == "medication_gimo":
                self.medication_status_score = '1'
            if self.medication_status_value == "medication_multiple_drugs":
                self.medication_status_score = '1'           
           

    @api.depends('history_fall_value','physical_status_value','mental_status_value','medication_status_value')
    def _fall_risk_final_total(self):
        self.fall_risk_final_total = self.history_fall_score + self.physical_status_score + self.mental_status_score + self.medication_status_score

    
    @api.onchange('fall_risk_final_total')
    def onchange_fall_risk_final_total(self):
        if self.fall_risk_final_total > 5:
            self.msg = _('Potential Risk for falls')
        else:
            self.msg = ''

    @api.onchange('eye_value')
    def onchange_eye_selection(self):
            if self.eye_value == "spotaneously":
                self.eye_score = '4'
            elif self.eye_value == "to_speech":
                self.eye_score = '3'
            elif self.eye_value == "to_pain":
                self.eye_score = '2'
            elif self.eye_value == "no_response":
                self.eye_score = '1'
            else:
                self.eye_score = '0'
                
    @api.onchange('best_verbal_value')
    def onchange_verbal_selection(self):
            if self.best_verbal_value == "oriented_time_person":
                self.best_verbal_score = '5'
            elif self.best_verbal_value == "confused":
                self.best_verbal_score = '4'
            elif self.best_verbal_value == "inappropriated_words":
                self.best_verbal_score = '3'
            elif self.best_verbal_value == "incomprehensible_sounds":
                self.best_verbal_score = '2'
            elif self.best_verbal_value == "no_response":
                self.best_verbal_score = '1'
            else:
                self.best_verbal_score = '0'
                
                
    @api.onchange('best_motor_value')
    def onchange_motor_selection(self):
            if self.best_motor_value == "obeys_commands":
                self.best_motor_score = '6'
            elif self.best_motor_value == "moves_localized":
                self.best_motor_score = '5'
            elif self.best_motor_value == "flexion_drawal":
                self.best_motor_score = '4'
            elif self.best_motor_value == "abnornal_flexion":
                self.best_motor_score = '3'
            elif self.best_motor_value == "abnormal_extension":
                self.best_motor_score = '2'
            elif self.best_motor_value == "no_response":
                self.best_motor_score = '1'
            else:
                self.best_motor_score = '0'

    @api.depends('eye_value','best_verbal_value','best_motor_value')
    def _gcs_total(self):
        self.gcs_final_total = self.eye_score + self.best_verbal_score + self.best_motor_score
        if self.gcs_final_total == 0:
            self.gcs_na = True
        else:
            self.gcs_na = False


#Access R-S
class PainControl(models.Model):
    _name = 'pain.control'

    date = fields.Date('Date')
    time = fields.Char('Time')
    score = fields.Selection([
        ('no_hurt','0 - No Hurt'),('hurts_little_bit','2 - Hurts Little Bit'),
        ('hurts_little_more','4 - Hurts Little More'),('hurts_even_more','6 - Hurts Even More'),
        ('hurts_whole_lot','8 - Hurts Whole Lot'),('hurts_worst','10 - Hurts Worst')],string="Score")
    medicine_non_drug = fields.Char('medicine')
    score_after = fields.Selection([
        ('no_hurt','0 - No Hurt'),('hurts_little_bit','2 - Hurts Little Bit'),
        ('hurts_little_more','4 - Hurts Little More'),('hurts_even_more','6 - Hurts Even More'),
        ('hurts_whole_lot','8 - Hurts Whole Lot'),('hurts_worst','10 - Hurts Worst')],string="Score after 1 hour")
    sign_id = fields.Char('Sign & ID')
    non_drug = fields.Many2one('inpatient.registration')
 
class EffectPain(models.Model):
    _name = 'effect.pain'

    name = fields.Selection(dec_obj,'Name')
    decreased_fun = fields.Char(string="Decreased Function")
    effect_id = fields.Many2one('inpatient.registration')

class MedicationDetails(models.Model):
    _name = 'medications.detail'
    
    medication = fields.Many2one('product.product',string="Medication")
    frequency = fields.Many2one(related='medication.common_dosage',string="Frequency")
    timing = fields.Char(string="Timing")
    route = fields.Char(string="Route")
    remarks = fields.Char(string="Remarks")
    medication_detail_id = fields.Many2one('inpatient.registration')

class PostOperative(models.Model):
    _name = 'post.operation'

    post_ob = fields.Selection(selection_obj,string="Name")
    min_15 = fields.Char(string="15 min(1st Hr.)")
    min_30 = fields.Char(string="30 min(1st Hr.)")
    min_45 = fields.Char(string="45 min(1st Hr.)")
    min_60 = fields.Char(string="60 min(1st Hr.)")
    min_90 = fields.Char(string="90 min(2nd Hr.)")
    min_120 = fields.Char(string="120 min(1st Hr.)")
    min_180 = fields.Char(string="180 min(3rd Hr.)")
    min_240 = fields.Char(string="240 min(4th Hr.)")
    staff = fields.Many2one('inpatient.registration')

#Access R-S

class HistoryMedication(models.Model):
    _name = 'history.medication'

    product_id = fields.Char(string='Name of Medication')
    dosage = fields.Float(string='Dose')
    frequency = fields.Char(string='Frequency')
    advice_by = fields.Many2one('res.users',string='Advice by')
    history_medicatiion = fields.Many2one('inpatient.registration',string='History Medication')

#Access R-S
class VulnerableAssessment(models.Model):
    _name = 'vulnerable.assessment'

    name = fields.Char('Categories')
    yes = fields.Boolean('Yes')
    no = fields.Boolean('No')
    cat_id = fields.Many2one('inpatient.registration')


class DailyLiving(models.Model):
    _name = 'daily.living'

    activity = fields.Selection(act_obj,'Activity')
    usual_level = fields.Char('Usual Level')
    level_on_add = fields.Char('Level On Admission')
    a_daily_living = fields.Many2one('inpatient.registration')

#Access R-S


class VitalIOChart(models.Model):
    _name = 'vitals.io.chart'

    time = fields.Selection(selection_time,'Time')
    vitals_temp = fields.Float(string="Temp")
    vitals_pulse = fields.Float(string="Pulse")
    vitals_resp = fields.Float(string="Resp")
    vitals_bp = fields.Float(string="BP")
    vitals_spo2 = fields.Float(string="SPO2")
    vitals_oral = fields.Float(string="Oral")
    vitals_ng_rtf_jft = fields.Float(string="NG/RTF/JFT")
    vitals_iv1 = fields.Float(string="IV1")
    vitals_iv2 = fields.Float(string="IV2")
    vitals_tpn = fields.Float(string="TPN")
    intake_hourly_total = fields.Float(string="Input Total")
    vitals_rta = fields.Float(string="RTA")
    vitals_urine = fields.Float(string="Urine")
    vitals_vomit = fields.Float(string="Vomit")
    vitals_stool = fields.Float(string="Stool")
    vitals_icd1 = fields.Float(string="ICD1")
    vitals_icd2 = fields.Float(string="ICD2/PCD")
    output_hourly_total = fields.Float(string="Output Total")    
    careplan_hms_id = fields.Many2one('inpatient.registration',string="VITALS")

    @api.onchange('vitals_oral','vitals_ng_rtf_jft','vitals_iv1','vitals_iv2','vitals_tpn','vitals_rta','vitals_urine','vitals_vomit','vitals_stool','vitals_icd1','vitals_icd2')
    def on_total_hourly(self):
       self.intake_hourly_total = float(self.vitals_oral) + float(self.vitals_ng_rtf_jft) + float(self.vitals_iv1) + float(self.vitals_iv2) + float(self.vitals_tpn)
       self.output_hourly_total = float(self.vitals_rta) + float(self.vitals_urine) + float(self.vitals_vomit) + float(self.vitals_stool) + float(self.vitals_icd1) + float(self.vitals_icd2) 

class NursingMasterChart(models.Model):
    _name = 'nursing.io.chart'

    nursing_date = fields.Date(string='Date', default=fields.Datetime.now)
    nursing_time = fields.Float(string='Time')
    nursing_weight = fields.Float(string='Weight')
    nursing_time_avg_hrly = fields.Float(string='Time & AG 6 Hrly')
    nursing_total_oral = fields.Float(string='Total Oral')
    nursing_total_iv = fields.Float(string='Total I.V')
    nursing_total_jft = fields.Float(string='Total JFT/RTF')
    nursing_total_intake = fields.Float(string='Total In Take')
    nursing_uo = fields.Float(string='U/O')
    nursing_stool = fields.Float(string='Stool')
    nursing_rta = fields.Float(string='RTA')
    nursing_drain_one = fields.Float(string='Drain 1')
    nursing_drain_two = fields.Float(string='Drain 2')
    nursing_ib_cb = fields.Float(string='I.B./C.B.')
    nursing_pcd = fields.Float(string='PCD')
    nursing_total_output = fields.Float(string='Total Output')
    nursing_bal = fields.Float(string='Balance')
    nursing_sign_of_staff = fields.Many2one('res.users',string='Sign of Staff/Incharge', default=lambda self: self.env.user, readonly="1")
    nursing_chart_ids = fields.Many2one('inpatient.registration')

class MasterChart(models.Model):
    _name = 'master.chart'

    careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    master_datetime = fields.Datetime(string="Date & Time", default=fields.datetime.today())
    t1_ag = fields.Datetime(string="Time 1")
    ag1 = fields.Float(string="AG1")
    t2_ag = fields.Datetime(string="Time 1")
    ag2 = fields.Float(string="AG1")
    t3_ag = fields.Datetime(string="Time 1")
    ag3 = fields.Float(string="AG1")
    t4_ag = fields.Datetime(string="Time 1")
    ag4 = fields.Float(string="AG1")
    master_weight = fields.Float(string="Weight")
    total_oral = fields.Char(string="Total Oral")
    total_iv = fields.Char(string="Total I.V.")
    jft_rtf = fields.Char(string="Total JFT/RTF")
    total_intake = fields.Char(string="Total Intake")
    u_o = fields.Char(string="U/O")
    stool = fields.Char(string="Stool")
    rta = fields.Char(string="RTA")
    drain1 = fields.Char(string="Drain 1")
    drain2 = fields.Char(string="Drain 2")
    ib_cb = fields.Char(string="I.B./C.B.")
    pcd = fields.Char(string="PCD")
    total_output = fields.Char(string="Total Output")
    balance = fields.Char(string="Balance")
    master_chart_user = fields.Many2one('res.users','User', default=lambda self: self.env.user, readonly="1")

# class PreoperativeInvestigation(models.Model):
#     _name = 'preoperative.investigation'

#     careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
#     name = fields.Char(string="Investigation", readonly="1")
#     preop_done = fields.Boolean(string="Yes / No")
#     copy_no = fields.Integer(string="No of copies")

# class PreoperativeInformation(models.Model):
#     _name = 'preoperative.information'

#     careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
#     name = fields.Char(string="Content", readonly="1")
#     info_done = fields.Boolean(string="Yes / No")

class ServiceProvided(models.Model):
    _name = 'service.provided'

    careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    service_datetime = fields.Datetime(string="Date & Time")
    service_description = fields.Char(string="Service Description")
    service_pro_name = fields.Many2one('res.users','Service Provider Name', default=lambda self: self.env.user, readonly="1")

class MorningShift(models.Model):
    _name = 'morning.shift'

    careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    morning_shift = fields.Char()
    morning_date = fields.Datetime(string="Date", default=fields.datetime.today())
    m_nurse_username = fields.Many2one('res.users','User', default=lambda self: self.env.user, readonly="1")

class EveningShift(models.Model):
    _name = 'evening.shift'

    careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    evening_shift = fields.Char()
    evening_date = fields.Datetime(string="Date", default=fields.datetime.today())
    e_nurse_username = fields.Many2one('res.users','User', default=lambda self: self.env.user, readonly="1")

class NightShift(models.Model):
    _name = 'night.shift'

    careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    night_shift = fields.Char()
    night_date = fields.Datetime(string="Date", default=fields.datetime.today())
    n_nurse_username = fields.Many2one('res.users','User', default=lambda self: self.env.user, readonly="1")

class InterventionObservation(models.Model):
    _name = 'intervention.observation'

    careplan_hms_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    observ_time = fields.Datetime(string="Time", default=fields.datetime.now())
    temp_inter = fields.Char(string="Temperature")
    pulse_inter = fields.Char(string="Pulse")
    rr_inter = fields.Char(string="RR")
    bp_inter = fields.Char(string="BP")
    o2_sat = fields.Char(string="O2 Sat")
#    pain_inter = fields.Char(string="Pain")

class TreatmentERDepartment(models.Model):
    _name = 'treatment.er.department'

    name = fields.Many2one('res.users','Name')
    treatment_er_department_id = fields.Many2one('inpatient.registration',string='Treatment Er Department')

class NusringPastHistory(models.Model):
    _name = 'nusring.past.history'

    name = fields.Char(string='Name')
    value = fields.Selection([('yes','Yes'),('no','No')],default='no',string='Yes/No')
    nursing_past_history_id = fields.Many2one('inpatient.registration',string='Family History')


class NusringFamilyHistory(models.Model):
    _name = 'nusring.family.history'

    name = fields.Char(string='Name')
    father = fields.Boolean(string='Father',default=False)
    mother = fields.Boolean(string='Mother',default=False)
    brother = fields.Boolean(string='Brother',default=False)
    sister = fields.Boolean(string='Sister',default=False)
    duration = fields.Char(string='Duration')
    value = fields.Selection([('yes','Yes'),('no','No')],default='no',string='Yes/No')
    nursing_family_history_id = fields.Many2one('inpatient.registration',string='Family History')


    @api.onchange('father','mother','brother','sister')
    def onchange_family_history(self):
        if self.father == True:
            self.value = 'yes'
        if self.mother == True:
            self.value = 'yes'
        if self.brother == True:
            self.value = 'yes'
        if self.mother == True:
            self.value = 'yes'
