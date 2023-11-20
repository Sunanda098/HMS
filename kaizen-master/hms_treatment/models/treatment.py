# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _
from openerp.exceptions import UserError
import dateutil.relativedelta
import random
import pytz
from openerp import SUPERUSER_ID

class IndimediTreatment(models.Model):
    _name = 'hms.treatment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hms.patient', 'Patient')
    sex = fields.Selection(related='patient_id.sex', string='sex')
    treatment_date = fields.Datetime(string='Date', default=fields.Datetime.now)
    diagnosis_id = fields.Many2one('hms.diseases',string='Diagnosis')
    pres_group_id = fields.Many2one('prescription.group',string='Group')
    primary_doctor = fields.Many2one(related='patient_id.primary_doctor',string='Treating Doctor')
    attending_physician_ids = fields.Many2many('hms.physician','hosp_treat_doc_rel','treat_id','doc_id',string='Attending Doctor')
    prescription_line = fields.One2many('prescription.line', 'treatment_id','Prescription')
    tproduct_id = fields.Many2one(related='prescription_line.product_id',ondelete='restrict',string='Product')
    tproduct_unit = fields.Char(related='prescription_line.product_unit',string='Unit')
    tproduct_days = fields.Integer(related='prescription_line.days',string='Days')
    tproduct_dose = fields.Float(related='prescription_line.dose',string='Dose')
    tproduct_route_treat = fields.Selection(related='prescription_line.route_treat',string='Route')
    tproduct_common_doseage = fields.Many2one(related='prescription_line.common_dosage',string='Frequency')
    finding = fields.Text(string="Diet")
    physiotherapy = fields.Text(string="Physiotherapy")
    lab_group_id = fields.Many2one('hms.investigation.group',string='Laboratory Group')
    radio_group_id = fields.Many2one('hms.investigation.group',string='Radiology Group')
    radiology_line = fields.One2many('hms.investigation.radiology.line', 'treatment_id', string='Radiology')
    pathology_line = fields.One2many('hms.investigation.pathology.line', 'treatment_id', string='Pathology')
    manometry_line = fields.One2many('hms.investigation.manometry.line', 'treatment_id', string='Manometry')
    endoscopy_line = fields.One2many('hms.investigation.endoscopy.line', 'treatment_id', string='Endoscopy')
    instruction = fields.One2many('ipd.instruction', 'treatment_id', string='Instruction')
    medical_emergency = fields.Boolean(string='Is Medical Emergency')
    hospitalization_id = fields.Many2one('inpatient.registration',string='Hospitalization')
    hospitalization_ids = fields.Many2one('inpatient.registration',string='Hospitalization')
    instruction_group_id = fields.Many2one('ipd.instruction.group',string="Instruction Group")
    fill = fields.Text(string='Filled')
    active = fields.Boolean("Active", default=True, track_visibility='always')
    rbs_line = fields.One2many('rbs.line', 'treatment_id', string="RBS")
    
    # @api.onchange('instruction_group_id')
    # def onchange_instruction_group_id(self):
    #     if self.patient_id and self.patient_id.sex ==self.instruction_group_id.gender:
    #         self.instruction = self.instruction_group_id.ipd_instruction_ids
    #     else:
    #         self.instruction = False


    @api.multi
    def toggle_active(self):
        self.active = not self.active
        treatment_ids = self.env['prescription.line.treatment'].search([('active', '=', not self.active),('line_id', 'in', self.prescription_line.ids)])
        for sheet in treatment_ids:
            if not sheet.completed:
                sheet.active = self.active

    @api.model
    def create(self, values):
        res = super(IndimediTreatment, self).create(values)
        for line in res.prescription_line:
            next_val = 0
            t_val = []
            if line.t1:
                t_val.append('t1')
            if line.t2:
                t_val.append('t2')
            if line.t3:
                t_val.append('t3')
            if line.t4:
                t_val.append('t4')
            if t_val:
                date_time = datetime.now()
                for dose in range(1, int(line.days+1)*int(line.common_dosage.code)):
                    t1 = eval('line.'+t_val[next_val])
                    if int(t1) == 24:
                        date_val = datetime.strptime(date_time.strftime('%Y-%m-%d %H:00:00'), '%Y-%m-%d %H:00:00').replace(hour=23, minute=59)+timedelta(hours=-5, minutes=-30)
                    else:
                        date_val = datetime.strptime(date_time.strftime('%Y-%m-%d %H:00:00'), '%Y-%m-%d %H:00:00').replace(hour=int(t1))+timedelta(hours=-5, minutes=-30)
                    next_val += 1
                    if len(t_val) == next_val:
                        next_val = 0
                        date_time = date_time + timedelta(days=1)

                    line.write({
                        'treatment_ids': [(0, 0, {
                            'line_id': line.id,
                            't1': t1,
                            'date_time': date_val,
                            'patient_id': res.patient_id.id,
                        })]
                    })
        self.env['prescription.line.treatment']._cron_next_treatment()
        return res

    
    def get_treatment_date(self,obj):
        tz = pytz.timezone(self.env.user.partner_id.tz) or pytz.utc
        if obj.treatment_date:
            treatment_date = pytz.utc.localize(datetime.strptime(obj.treatment_date, "%Y-%m-%d %H:%M:%S")).astimezone(tz)
            treatment_date.replace(tzinfo=None)
            return treatment_date.replace(tzinfo=None)

    @api.onchange('pres_group_id')
    def on_change_pres_group_id(self):
        product_lines = []
        group_obj = self.env['medicament.group.line']
        for group in self.pres_group_id.group_line:
            lines = []
            for medicament in group.medicament_group_id.medicine_list:
                lines.append(medicament.id)
            limit = 0
            if group.medicament_group_id.limit > len(lines):
                limit = len(lines)
            else:
                limit = group.medicament_group_id.limit
            list_l = random.sample(lines, limit)
            for line in group_obj.browse(list_l):
                product_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'common_dosage': line.common_dosage.id,
                    'days': line.days,
                    'quantity' : line.quantity,
                    'actual_time':datetime.now(),
                    't1':line.common_dosage.t1,
                    't2':line.common_dosage.t2,
                    't3':line.common_dosage.t3,
                    't4':line.common_dosage.t4,
                }))
        if self.fill != 'Filled':
            treatment_ids = self.env['hms.treatment'].search([('hospitalization_id','=',self._context['default_hospitalization_id'])])
            if treatment_ids:
                latest_treatment_id = max(treatment_ids.ids)
                treatment = self.env['hms.treatment'].browse(latest_treatment_id)
                product_lines = []
                for rec in treatment.prescription_line:
                    product_lines.append((0,0,{
                        'product_id':rec.product_id.id,
                        'dose' : rec.dose,
                        'actual_time':rec.actual_time,
                        'common_dosage': rec.common_dosage.id,
                        't1':rec.t1,
                        't2':rec.t2,
                        't3':rec.t3,
                        't4':rec.t4,
                        'quantity' : rec.quantity,
                        'stat':rec.stat,
                        'days':rec.days,
                    }))
            self.fill = 'Filled'
        self.prescription_line =  product_lines

    @api.onchange('lab_group_id')
    def on_change_lab_group_id(self):
        if self.lab_group_id.investigation_type == 'pathology':
            product_lines = []
            for line in self.lab_group_id.group_line:
                product_lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'price': line.price,
                    'inv_username': line.env.user.name,
                    'instruction': line.instruction,
                }))
            self.pathology_line = product_lines

        if self.lab_group_id.investigation_type == 'radiology':
            product_lines = []
            for line in self.lab_group_id.group_line:
                product_lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'price': line.price,
                    'instruction': line.instruction,
                }))
            self.radiology_line = product_lines

        if self.lab_group_id.investigation_type == 'manometry':
            product_lines = []
            for line in self.lab_group_id.group_line:
                product_lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'price': line.price,
                    'instruction': line.instruction,
                }))
            self.manometry_line = product_lines

        if self.lab_group_id.investigation_type == 'endoscopy':
            product_lines = []
            for line in self.lab_group_id.group_line:
                product_lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'price': line.price,
                    'instruction': line.instruction,
                }))
            self.endoscopy_line = product_lines

        if self.lab_group_id.investigation_type == 'os':
            product_lines = []
            for line in self.lab_group_id.group_line:
                product_lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'price': line.price,
                    'instruction': line.instruction,
                }))
            self.other_services_line = product_lines

        if self.lab_group_id.investigation_type == 'all':
            rad_product_lines = []
            path_product_lines = []
            endo_product_lines = []
            mano_product_lines = []
            os_product_lines = []
            for line in self.lab_group_id.group_line:
                if line.product_id.hospital_product_type == 'radiology':
                    rad_product_lines.append((0,0,{
                        'product_id': line.product_id.id,
                        'price': line.price,
                        'instruction': line.instruction,
                    }))
                    self.radiology_line = rad_product_lines
                if line.product_id.hospital_product_type == 'pathology':
                    path_product_lines.append((0,0,{
                        'product_id': line.product_id.id,
                        'price': line.price,
                        'instruction': line.instruction,
                    }))
                    self.pathology_line = path_product_lines
                if line.product_id.hospital_product_type == 'endoscopy':
                    endo_product_lines.append((0,0,{
                        'product_id': line.product_id.id,
                        'price': line.price,
                        'instruction': line.instruction,
                    }))
                self.endoscopy_line = endo_product_lines
                if line.product_id.hospital_product_type == 'manometry':
                    mano_product_lines.append((0,0,{
                        'product_id': line.product_id.id,
                        'price': line.price,
                        'instruction': line.instruction,
                    }))
                self.manometry_line = mano_product_lines
                if line.product_id.hospital_product_type == 'os':
                    os_product_lines.append((0,0,{
                        'product_id': line.product_id.id,
                        'price': line.price,
                        'instruction': line.instruction,
                    }))
                self.other_services_line = os_product_lines

class PathologyLine(models.Model):
    _inherit = 'hms.investigation.pathology.line'

    treatment_id = fields.Many2one('hms.treatment', 'Treatment')

class RadiologyLine(models.Model):
    _inherit = 'hms.investigation.radiology.line'

    treatment_id = fields.Many2one('hms.treatment', 'Treatment')

class EndoscopyLine(models.Model):
    _inherit = 'hms.investigation.endoscopy.line'

    treatment_id = fields.Many2one('hms.treatment', 'Treatment')

class ManometryLine(models.Model):
    _inherit = 'hms.investigation.manometry.line'

    treatment_id = fields.Many2one('hms.treatment', 'Treatment')

class RbsLine(models.Model):
    _name = 'rbs.line'

    treatment_id = fields.Many2one('hms.treatment', 'Treatment')
    rbs_time = fields.Datetime(string="Time")
    rbs_value = fields.Char(string="Value")
    rbs_insulin = fields.Char(string="Insulin")
    
class IndimediPrescriptionLine(models.Model):
    _inherit = 'prescription.line'

    treatment_id = fields.Many2one('hms.treatment', 'Treatment')
    product_unit = fields.Char(string='Unit')
    hospitalization_id = fields.Many2one('inpatient.registration',string='Hospitalization')
    appointment_id = fields.Many2one('hms.appointment',string='Appointment')
    treatment_ids = fields.One2many('prescription.line.treatment', 'line_id', 'Treatment')
    route_treat = fields.Selection([('iv','IV'),('im','IM'),('sc','SC')], string="Route")
    t5 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')], string="T5")
    t6 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')], string="T6")


class IndimediIPDInstruction(models.Model):
    _inherit = 'ipd.instruction'

    treatment_id = fields.Many2one('hms.treatment', 'Treatment')

class Hospitalization(models.Model):
    _inherit = "inpatient.registration"

    treatment_ids = fields.One2many('hms.treatment', 'hospitalization_id','Treatment')
    medicine_at_home_ids = fields.One2many('prescription.line', 'hospitalization_id','Treatment on Discharge')
    care_plan = fields.Char(string="Plan of Care")
    discharge_inv = fields.Char(string="Investigations")
    pending_report = fields.Char(string="Pending Reports")
    histo_report = fields.Char(string="Histopatho Reports")
    admission_weight = fields.Char(string="Weight on Admission")
    discharge_weight = fields.Char(string="Weight on Discharge")
    histo_report = fields.Char(string="Histopatho Reports")   
    diet = fields.Char(string="Diet")
    gen_advice = fields.Char(string="General Advice")
    warning = fields.Char(string="Warning Signs & Symptoms")
    mo_summary = fields.Char(string="M.O. Preparing Summary")
    follow_datetime = fields.Datetime(string="Follow Up Date Time")

    @api.multi
    def view_discharge_summary(self):
        res = super(Hospitalization, self).view_discharge_summary()
        treatment_obj = self.env['hms.treatment']
        for rec in self:
            rec.medicine_at_home_ids = False
            for history in rec.accomodation_history_ids:
                if self.bed_id == history.bed_id:
                    history.end_date = datetime.now()
            if rec.treatment_ids:
                latest_treatment_id = max(rec.treatment_ids.ids)
                treatment = treatment_obj.browse(latest_treatment_id)
                if treatment.prescription_line:
                    new_prescription_line = treatment.prescription_line.copy()
                    new_prescription_line.write({'hospitalization_id' : treatment.hospitalization_id.id})
                    new_prescription_line.write({'treatment_id' : False})
        return res

class Appointment(models.Model):
    _inherit = 'hms.appointment'

    medicine_at_home_ids = fields.One2many('prescription.line', 'hos_appointment_id','Treatment on Discharge')
    personal_his = fields.Char('Description')
    personal_his_ids = fields.One2many('appointment.history', 'appointment_id', string='Personal History')

    @api.depends('patient_id')
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        res = super(Appointment, self).onchange_patient_id()
        inpatient_obj = self.env['inpatient.registration']
        hospitalization_ids = inpatient_obj.search([('patient_id','=',self.patient_id.id),('state','in',['done','discharged'])])
        self.medicine_at_home_ids = False
        if hospitalization_ids:
            latest_hospitalization_id = max(hospitalization_ids.ids)
            inpatient = inpatient_obj.browse(latest_hospitalization_id)
            self.medicine_at_home_ids = inpatient.medicine_at_home_ids
        return res

class PersonalHistory(models.Model):
    _name = 'appointment.history'

    appointment_id = fields.Many2one('hms.appointment','Appointment')
    personal_his_id = fields.Many2one('personal.history','Personal History')
    personal_his = fields.Char('Description')

class History(models.Model):
    _name = 'personal.history'

    name = fields.Char('History')

class PrescriptionLineTreatment(models.Model):
    _name = 'prescription.line.treatment'
    _order = 'patient_id,date_time'

    line_id = fields.Many2one('prescription.line', string='Prescription Line')
    patient_id = fields.Many2one('hms.patient', string='Patient')
    bed_id = fields.Many2one(related='line_id.treatment_id.hospitalization_id.bed_id', string="Bed")
    product_id = fields.Many2one(related='line_id.product_id', string="Medicine")
    dose = fields.Float(related='line_id.dose', string="Dosage")
    common_dosage = fields.Many2one(related='line_id.common_dosage', string="Common Dosage")
    suffix_frequency_id = fields.Many2one(related='line_id.product_id.suffix_frequency_id', string="Common Dosage")
    date_time = fields.Datetime('Exc Time')
    exc_time = fields.Datetime('Excuted Time')
    completed = fields.Boolean('Completed', default=False)
    next_treatment = fields.Boolean(string='Next Treatment', default=False)
    state = fields.Selection([('Normal', 'Normal'), ('Danger', 'Danger')], string="State", default="Normal")
    t1 = fields.Selection([
                           ('1','1AM'),
                           ('2','2AM'),
                           ('3','3AM'),
                           ('4','4AM'),
                           ('5','5AM'),
                           ('6','6AM'),
                           ('7','7AM'),
                           ('8','8AM'),
                           ('9','9AM'),
                           ('10','10AM'),
                           ('11','11AM'),
                           ('12','12AM'),
                           ('13','1PM'),
                           ('14','2PM'),
                           ('15','3PM'),
                           ('16','4PM'),
                           ('17','5PM'),
                           ('18','6PM'),
                           ('19','7PM'),
                           ('20','8PM'),
                           ('21','9PM'),
                           ('22','10PM'),
                           ('23','11PM'),
                           ('24','12PM')], string="T1")
    active = fields.Boolean("Active/Deactive", default=True)


    @api.multi
    def medicine_done(self):
        self.completed = True
        self.exc_time = datetime.now()

    @api.multi
    def medicine_undone(self):
        self.completed = False


    @api.multi
    def _cron_next_treatment(self):
        self.search([('next_treatment', '=', True)]).write({'next_treatment': False, 'state': 'Normal'})
        domain = [
            ('active', '=', True),
            ('date_time', '>', (datetime.now()-timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')),
            ('date_time', '<', (datetime.now()+timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'))
        ]
        treatment_ids =  self.search(domain)
        for treatment in treatment_ids:
            if treatment.date_time < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                treatment.state = 'Danger'
            treatment.next_treatment = True
