 # -*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import datetime ,date 

class IndimediIPDOpnoteComments(models.Model):
    _name = "indimedi.ipd.opnote.comments"
    _description = "IPD Opnote Comments"
    
    name = fields.Char(string='Comments',required=True)

class IndimediIPDOpnoteOtnote(models.Model):
    _name = "indimedi.ipd.opnote.otnote"
    _description = "IPD OT  Note"
    
    name = fields.Char(string='OT Note',required=True)

class IndimediIPDOpnoteDrainage(models.Model):
    _name = "indimedi.ipd.opnote.drainage"
    _description = "IPD Drainage"
    
    name = fields.Char(string='Drainage',required=True)

class IndimediIPDOpnoteClosure(models.Model):
    _name = "indimedi.ipd.opnote.closure"
    _description = "IPD Closure"
    
    name = fields.Char(string='Closure',required=True)

class IndimediIPDOpnoteHistopathology(models.Model):
    _name = "indimedi.ipd.opnote.histopathology"
    _description = "IPD OT  Note"
    
    name = fields.Char(string='Histopathology',required=True)


class IndimediIPDOpnoteFellow(models.Model):
    _name = "indimedi.ipd.discharge.fellow"
    _description = "IPD Opnote Fellow"
    
    name = fields.Char(string='Fellow',required=True)

class IndimediDiagnosis(models.Model):
	_name="indimedi.diagonsis"

	name = fields.Char('Diagnosis')

class MedicalHistory(models.Model):
	_name="medical.history"

	name = fields.Char('Medical History')

class Asa(models.Model):
	_name = 'indimedi.asa'

	name = fields.Char('Asa')

class PreMedication(models.Model):
	_name = 'indimedi.pre.medication'

	name = fields.Char('Pre Medication')

class PreOperativeProcedure(models.Model):
	_name = 'pre.operative.procedure'

	name = fields.Char('Pre Operative Procedure')

class PositionPatient(models.Model):
	_name = 'position.patient'

	name = fields.Char('Position Of Patient')

class AnaesthiaTechnique(models.Model):
    _name = 'anaesthesia.technique'

    name = fields.Char('Anaesthesia Techique')

class AnaesthiaTechnique(models.Model):
    _name = 'anaesthesia.agent'

    name = fields.Char('Inducing Agent')

class AnaesthesiaMuscle(models.Model):
    _name = 'anaesthesia.muscle'

    name = fields.Char('Anaesthesia Muscle')

class LaryngoscopyRefex(models.Model):
    _name = 'laryngoscopy.refex'

    name = fields.Char('Laryngoscopy Refex Attenuation')

class EtLml(models.Model):
    _name = 'et.lml.dlt'

    name = fields.Char('ET Tube/LML/DLT')

class InhalationAgent(models.Model):
    _name = 'inhalation.agent'

    name = fields.Char('Inhalation Agent')

class ApnCircuit(models.Model):
    _name = 'apn.circuit'

    name = fields.Char('Circuit')

class ApnVentilation(models.Model):
    _name = 'apn.ventilation'

    name = fields.Char('Ventilation')

class ApnSpinal(models.Model):
    _name = 'apn.spinal'

    name = fields.Char('Spinal')

class ApnEpidural(models.Model):
    _name = 'apn.epidural'

    name = fields.Char('Epidural')

class ApnBlockl(models.Model):
    _name = 'apn.block'

    name = fields.Char('Block')

class IntraOp(models.Model):
    _name = 'intra.op.complications'

    name = fields.Char('Intra-Op Complications')

class AnsnotePreopCourse(models.Model):
    _name = 'ansnote.pre.op.course'

    name = fields.Char('Pre-Op Course')

class AnsnotePostopCourse(models.Model):
    _name = 'ansnote.post.op.course'

    name = fields.Char('Post-Op Course')

class AnsnoteRiskFactor(models.Model):
    _name = 'ansnote.risk.factor'

    name = fields.Char('Risk Factor')

class AnsnoteMaintenance(models.Model):
    _name = 'ansnote.maintenance'

    name = fields.Char('Maintenance')

class PreMedication(models.Model):
    _name = 'indimedi.pre.anesthetic.medication'

    name = fields.Char('Pre-Anesthetic Medication')

class HmsIncision(models.Model):
    _name = 'hms.incision'
        
    name = fields.Char('Incision')

class HmsApproach(models.Model):
    _name = 'hms.approach'

    name = fields.Char('Approach') 

class ImplantSize(models.Model):
    _name = 'implant.size'

    name = fields.Char('Implant Size')

class IndimediHospitalization(models.Model):
    _inherit = "inpatient.registration"
#field for Apn    
    informed_consent = fields.Boolean('Informed Consent Taken')
    high_risk_consent = fields.Boolean('High Risk Consent Taken')
    relative_informed = fields.Boolean("Relative Informed")
    ot_time_in = fields.Datetime('O.T Time In')
    ot_time_out = fields.Datetime('O.T Time Out')
    ant_time_in = fields.Datetime('Anaesthia Time In')
    ant_time_out = fields.Datetime('Anaesthia Time Out')
    blood_group = fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')], string='Blood Group')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    medical_history_id = fields.Many2one('medical.history', ondelete="cascade", string='Positive Medical History')
    asa_id = fields.Many2one('indimedi.asa', ondelete="cascade", string="ASA")
    pre_medication_id = fields.Many2one('indimedi.pre.medication', ondelete="cascade", string="Pre Medication")
    pre_operation_id = fields.Many2one('pre.operative.procedure', ondelete="cascade", string="Pre Operative Procedure")
    position_patient_id = fields.Many2one('position.patient', ondelete="cascade", string="Position Of Patient")
    ana_technique_id = fields.Many2one('anaesthesia.technique', ondelete="cascade", string="Anaesthia Technique")
    anaesthesia_type = fields.Selection([('general','General Anaesthesia'),('regional','Regional Anaesthesia')], 'Anaesthesia')
    ana_inducing_id = fields.Many2one('anaesthesia.agent', ondelete="cascade", string="Inducing Agent")
    ana_muscle_relaxant_id = fields.Many2one('anaesthesia.muscle', ondelete="cascade", string="Muscle Relaxant")
    laryngoscopy_refex_id = fields.Many2one('laryngoscopy.refex', ondelete="cascade", string="Laryngoscopy Refex Attenuation")
    et_lml_id = fields.Many2one('et.lml.dlt', ondelete="cascade", string="ET Tube/LML/DLT")
    induction_id = fields.Many2one('apn.induction', ondelete="cascade", string="Induction")
    inhalation_agent_id = fields.Many2one('inhalation.agent', ondelete="cascade", string="Inhalation Agent")
    circuit_id = fields.Many2one('apn.circuit', ondelete="cascade", string="Circuit")
    ventilation_id = fields.Many2one('apn.ventilation', ondelete="cascade", string="Ventilation")
    reversal_id = fields.Many2one('apn.reversal', ondelete="cascade", string="Reversal")
    spinal_id = fields.Many2one('apn.spinal', ondelete="cascade", string="Spinal")
    epidural_id = fields.Many2one('apn.epidural', ondelete="cascade", string="Epidural")
    block_id = fields.Many2one('apn.block', ondelete="cascade", string="Block")
    intra_op_complications_id = fields.Many2one('intra.op.complications', ondelete="cascade", string="Intra-Op Complications")
    consciousness = fields.Char('Consciousness')
    pulse = fields.Char('Pulse')
    bp = fields.Char("B.P.")
    spo = fields.Char('SPO2')
    muscle_tone = fields.Char('Muscle Tone')
    pain = fields.Char('Pain')
    rt_aspiration = fields.Char("RT Aspiration")
    urine = fields.Char('Urine Output')
    rl = fields.Char('RL')
    ns = fields.Char('NS')
    dns = fields.Char("DNS")
    isolyte = fields.Char('Isolyte M/G/P')
    colloids = fields.Char('Colloids')
    transfusion = fields.Char('Transfusions')
    blood_loss = fields.Char("Blood Loss")
    remark = fields.Char('Remarks')
# Fields for Ans Note 
    ans_date = fields.Datetime(string='Date', default=fields.Datetime.now)
    risk_factor = fields.Many2one('ansnote.risk.factor',ondelete="cascade", string="Risk Factors")
    pre_anesthetic_medication_id = fields.Many2one('indimedi.pre.anesthetic.medication', ondelete="cascade", string="Pre-Anesthetic Medication")
    ans_induction_id = fields.Many2one('apn.induction', ondelete="cascade", string="Induction")
    ans_reversal_id = fields.Many2one('apn.reversal', ondelete="cascade", string="Reversal")
    maintenance_id = fields.Many2one('ansnote.maintenance',ondelete="cascade", string="Maintenance")
    pre_op_course_id = fields.Many2one('ansnote.pre.op.course', ondelete="cascade", string="Pre-Op Course")
    post_op_course_id = fields.Many2one('ansnote.post.op.course', ondelete="cascade", string="Post-Op Course")
    eng_inst = fields.Text(string="English") 
    hindi_inst = fields.Text(string="Hindi")
    guj_inst = fields.Text(string="Gujarati")
#for operative notes
    op_note_date = fields.Datetime(string="Date & Time")
    duration = fields.Char(string="Duration (in mins)")
    fellow = fields.Many2one('indimedi.ipd.discharge.fellow',ondelete="cascade", string="Fellow")
    employee = fields.Char(string="Employees")
    co_person = fields.Char(string="Company Person")
    observors = fields.Many2one('res.users',ondelete="cascade", string="Observors",domain=[('is_observer','=',True)])
    total_no_in_ot = fields.Char(string="Total No. in OT")
    side = fields.Selection([('left','Left'),('right','Right'),('other','Other')],string="Side")
    fracture_table = fields.Char(string="Fracture Table")
    iitv = fields.Char(string="IITV")
    position = fields.Char(string="Position")
    incision = fields.Many2one('hms.incision', string='Incision')
    approach = fields.Many2one('hms.approach', string="Approach")
    findings = fields.Text(string="Findings")
    procedure = fields.Text(string="Procedure")
    co_morbidity = fields.Many2many('hms.diseases','rel_disease_co_morbidity','patient_id','co_morbidity', string="Co Morbidity")
    allergy = fields.Char(string="Allergy")
    implant_name = fields.Many2one('hms.implant', ondelete="cascade", string='Implant')
    implant_company = fields.Many2one('implant.company', ondelete="cascade", string='Implant Company')
    distributor = fields.Char(string="Distributor")
    implant_size = fields.Many2one('implant.size', string="Implant Size")
    histopathology = fields.Many2one('indimedi.ipd.opnote.histopathology',ondelete="cascade", string="Specimen of HP")
    drainage = fields.Many2one('indimedi.ipd.opnote.drainage',ondelete="cascade", string="Drainage")
    closure = fields.Many2one('indimedi.ipd.opnote.closure',ondelete="cascade", string="Closure")
    ot_note = fields.Many2one('indimedi.ipd.opnote.otnote',ondelete="cascade", string="OT Note")
    morbidity_check = fields.Boolean('Morbidity')
    morbidity_ids = fields.One2many('operative.morbidity','inpatient_id', string="Morbidity")
    
#     op_note = fields.Text(string="OP. Note")
    opd_note = fields.Text(string="OPD Note")
    comments = fields.Many2one('indimedi.ipd.opnote.comments',ondelete="cascade", string="Comments")
    complications = fields.Char(string="Complications")
    extra_surgeries_ids = fields.One2many('hms.extrasurgeries','inpatient_id', string="Additional Surgeries")
    invesigation_ids =  fields.One2many('careplan.investigation', 'careplan_investigation_id', string="Investigation")

class OperativeMorbidity(models.Model):
    _name = 'operative.morbidity'

    inpatient_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    morbidity_id = fields.Many2one('surgery.morbidity', string="Morbidity")
    morbidity_info = fields.Char(string="Description")

class SurgeryMorbidity(models.Model):
    _name = 'surgery.morbidity'

    name = fields.Char('Morbidity')

class HmsExtrasurgeries(models.Model):
    _name = 'hms.extrasurgeries'

    surgery_id = fields.Many2many('hms_surgery','hosp_patient_surgery','hosp_id','surgery_id', ondelete="restrict", string='Surgery')
    patient_id = fields.Many2one('hms.patient', ondelete="restrict", string='Patient')
    sur_department_id = fields.Many2one(related='patient_id.department_id', ondelete="restrict", string='Department')
    hospital_ot = fields.Many2one('indimedi.hospital.or', ondelete="restrict", string='Operation Theatre')
    start_date = fields.Datetime(string='Surgery Date')
    end_date = fields.Datetime(string='End Date')
    #primary_physician = fields.Many2one ('hms.physician', ondelete="restrict", string='Primary Surgeon')
    primary_physician_ids = fields.Many2many('hms.physician','hosp_pri_doc_rel','hosp_id','doc_id',string='Primary Surgeons')
    assisting_surgeons = fields.Many2many('hms.physician','hosp_doc_rel','hosp_id','doc_id',string='Assisting Surgeons')
    user_id = fields.Many2many('res.users','hosp_user_id','surgery_id','anest_id', string='Anesthetist', ondelete="set null", help='Anesthetist data of the patient',domain=[('is_anesthetist','=',True)])
    scrub_nurse = fields.Many2one('res.users', ondelete="set null", string='Scrub Nurse',domain=[('is_nurse','=',True)])
    picking_type_id = fields.Many2one('stock.picking.type', ondelete="restrict", string='Picking Type')
    reason_id = fields.Many2one('hms.reason', ondelete="cascade", string='Reason')
    follow_date = fields.Datetime(string='Follow Up Date')
    anaesthesia_id = fields.Many2many('res.users','hosp_id','surgeries_id','user_anest_id', ondelete="set null", string="Anaesthesia")
    # op_note = fields.Text(string="OP. Note")
    inpatient_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    op_note_date = fields.Datetime(string="Date & Time")
    duration = fields.Char(string="Duration (in mins)")
    fellow = fields.Many2one('indimedi.ipd.discharge.fellow',ondelete="cascade", string="Fellow")
    employee = fields.Char(string="Employees")
    co_person = fields.Char(string="Company Person")
    observors = fields.Many2one('res.users',ondelete="cascade", string="Observors",domain=[('is_observer','=',True)])
    total_no_in_ot = fields.Char(string="Total No. in OT")
    side = fields.Selection([('left','Left'),('right','Right'),('other','Other')],string="Side")
    fracture_table = fields.Char(string="Fracture Table")
    iitv = fields.Char(string="IITV")
    position = fields.Char(string="Position")
    incision = fields.Many2one('hms.incision', string='Incision')
    approach = fields.Many2one('hms.approach', string="Approach")
    findings = fields.Text(string="Findings")
    procedure = fields.Text(string="Procedure")
    co_morbidity = fields.Many2many('hms.diseases','rel_surgery_co_morbidity','surgery_id','co_morbidity', string="Co Morbidity")
    allergy = fields.Char(string="Allergy")
    implant_name = fields.Many2one('hms.implant', ondelete="cascade", string='Implant')
    implant_company = fields.Many2one('implant.company', ondelete="cascade", string='Implant Company')
    distributor = fields.Char(string="Distributor")
    implant_size = fields.Many2one('implant.size', string="Implant Size")
    histopathology = fields.Many2one('indimedi.ipd.opnote.histopathology',ondelete="cascade", string="Specimen")
    drainage = fields.Many2one('indimedi.ipd.opnote.drainage',ondelete="cascade", string="Drainage")
    closure = fields.Many2one('indimedi.ipd.opnote.closure',ondelete="cascade", string="Closure")
    ot_note = fields.Many2one('indimedi.ipd.opnote.otnote',ondelete="cascade", string="OT Note")
#     op_note = fields.Text(string="OP. Note")
    opd_note = fields.Text(string="OPD Note")
    comments = fields.Many2one('indimedi.ipd.opnote.comments',ondelete="cascade", string="Comments")
    complications = fields.Char(string="Complications")

class CareplanInvestigation(models.Model):
    _name = 'careplan.investigation'
    _description = 'Care Investigation'
    _rec_name = 'careplan_investigation_id'

    careplan_investigation_id = fields.Many2one('inpatient.registration', ondelete="restrict", string="Hospitalization")
    date_investigation = fields.Datetime('Date', required="True",default=fields.Datetime.now)
    patient_id = fields.Many2one('hms.patient',ondelete="restrict", string='Patient')
    hb = fields.Char('Hb')
    bg = fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')], string='Blood Group')
    tc = fields.Char('TC')
    dc = fields.Char('DC')
    esr = fields.Char('ESR')
    peripheral_smear = fields.Char('Peripheral Smear')
    platelet_count = fields.Char('Platelet Count')
    bt_ct = fields.Char('BT/CT')
    urine = fields.Char('Urine R&M')
    fbs_rbs = fields.Char('FBS/RBS')
    ppbs = fields.Char('PPBS')
    urea = fields.Char('Urea')
    creatinine = fields.Char('Creatinine')
    na_plus = fields.Char('Na')
    k_plus = fields.Char('K')
    cl_minus = fields.Char('Cl')
    ca_plus = fields.Char('Ca')
    s_bili_direct = fields.Char('S.bilirubin-total(Direct)')
    s_bili_indirect = fields.Char('S.bilirubin-total(Indirect)')
    sgpt = fields.Char('SGPT')
    sgot = fields.Char('SGOT')
    s_alk = fields.Char('S.alkPO4')
    s_pro = fields.Char('S.protein-total')
    alb = fields.Char('Alb.')
    glob = fields.Char('Glob.')
    ag_ratio = fields.Char('A/G ratio')
    s_amylase = fields.Char('S.Amylase')
    s_lipase = fields.Char('S.Lipase')
    ldh = fields.Char('LDH')
    crp = fields.Char('CRP')
    pro_calcitonin = fields.Char('Pro Calcitonin')
    cea = fields.Char('CEA')
    afp = fields.Char('AFP')
    b12 = fields.Char('B12')
    vitamin_d3 = fields.Char('Vitamin D') 
    hiv = fields.Char('HIV')
    hbsg = fields.Char('HbsAg')
    aptt = fields.Char('APTT')
    pt = fields.Char('PT')
    # xray = fields.Char('X-Rays')
    # usg = fields.Char('USG')
    # mri = fields.Char('MRI/CT Scan')
    # ecg = fields.Char('ECG')
    # abg = fields.Char('ABG(Arterial Blood Gas)')
    # echo = fields.Char('Echo-Cardiography / TMT')
    # oth = fields.Char('Others')
    xray_inv = fields.Text('X-Rays')
    usg_inv = fields.Text('USG')
    mri_inv = fields.Text('MRI/CT Scan')
    ecg_inv = fields.Text('ECG')
    abg_inv = fields.Text('ABG(Arterial Blood Gas)')
    echo_inv = fields.Text('Echo-Cardiography / TMT')
    oth_inv = fields.Text('Others')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
