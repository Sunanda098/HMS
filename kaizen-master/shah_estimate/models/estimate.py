# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime


class HmsEstimate(models.Model):
    _name = "hms.estimate"
    _description = "Estimate"
    
    _rec_name = "patient_id"

    @api.model
    def _default_room_estimation(self):
        vals = []
        estimation = self.env['room.facility.charges'].search([])
        for room in estimation:
            vals.append((0, 0, {
                'name': room.name,
            }))
        return vals

    @api.model
    def _default_surgical_estimation(self):
        vals = []
        estimation = self.env['surgical.charges'].search([])
        for surgical in estimation:
            vals.append((0, 0, {
                'name': surgical.name,
            }))
        return vals

    @api.model
    def _default_operation_estimation(self):
        vals = []
        estimation = self.env['operation.equip.charges'].search([])
        for operation in estimation:
            vals.append((0, 0, {
                'name': operation.name,
            }))
        return vals

    @api.model
    def _default_investigation_estimation(self):
        vals = []
        estimation = self.env['investigation.pharmacy.charges'].search([])
        for investigation in estimation:
            vals.append((0, 0, {
                'name': investigation.name,
            }))
        return vals

    patient_id = fields.Many2one('hms.patient', ondelete="restrict", string='Patient')
    age = fields.Char(related="patient_id.age", string='Age')
    diagnosis_id = fields.Many2one('hms.diseases', ondelete='set null', string='Diagnosis')
    surgery_id = fields.Many2many('hms_surgery','hosp_patient_surgery','hosp_id','surgery_id', ondelete="restrict", string='Operation')
    admission_date = fields.Datetime('Admission Date', default=fields.Datetime.now)
    surgery_date = fields.Datetime('Surgery Date',default = fields.Datetime.now)
    expected_stay = fields.Char('Expected Stay')
    product_id = fields.Many2one('product.product', 'Package', domain=[('hospital_product_type', '=', 'package')])
    is_package = fields.Boolean('Is Package',default=True)
    estimate_lines = fields.One2many('hms.estimate.lines', 'estimate_id', string='Estimate Line')
    inpatient_id = fields.Many2one("inpatient.registration", ondelete="cascade", string="Hospitalization")
    estimate_price = fields.Float('Package Charges')
    consultant_id = fields.Many2one('hms.physician', string='Consultant')
    surgery_procedure = fields.Char(string='Surgery/Unplanned')
    case_type = fields.Selection([('planned', 'Planned'),('unplanned', 'Unplanned')], string='Case Type')
    surgery_grade = fields.Char('Surgery Grade')
    room_category = fields.Char('Room Category')
    room_facility_charges_ids = fields.One2many('room.facility.charges','room_facility_charges_id','Room Facility Charge',default=lambda self: self._default_room_estimation())
    surgical_charges_ids = fields.One2many('surgical.charges','surgical_charges_id','Surgical Charge',default=lambda self: self._default_surgical_estimation())
    operation_equip_charges_ids = fields.One2many('operation.equip.charges','operation_equip_charges_id','Operation Equip Charge',default=lambda self: self._default_operation_estimation())
    investigation_pharmacy_charges_ids = fields.One2many('investigation.pharmacy.charges','investigation_pharmacy_charges_id','Investigation & Pharmacy Charges',default=lambda self: self._default_investigation_estimation())
    hospitalization_id = fields.Many2one('inpatient.registration', string = 'Hospitalization')
    appointment_id = fields.Many2one('hms.appointment', string="Appointment")

    @api.onchange('product_id')
    def onchange_Product(self):
        if self.product_id:
            self.estimate_price = self.product_id.lst_price
            
    
    @api.multi
    def get_total(self):
        total = 0.0
        for est in self:
            for line in est.estimate_lines:
                total += line.amount
        return total
        
    @api.onchange('inpatient_id')
    def onchange_hospitalization(self):
        if self.inpatient_id:
            self.patient_id = self.inpatient_id.patient_id
            self.admission_date = self.inpatient_id.hospitalization_date
            self.diagnosis_id = self.inpatient_id.admission_reason
            self.surgery_id = self.inpatient_id.surgery_id
            self.expected_stay = self.inpatient_id.expected_stay
    

class HmsEstimateLines(models.Model):
    _name = "hms.estimate.lines"
    _description = "Estimate Lines"
   
    estimate_id = fields.Many2one('hms.estimate', ondelete='set null', string='estimate')
    product_id = fields.Many2one('product.product','Package', required=True, domain=[('hospital_product_type', '!=', 'insurance')])
    amount = fields.Float(string='Amount')
    
    

class Patient(models.Model):
    _inherit = "hms.patient"
    
    @api.multi
    def action_button_estimation(self):
        return {
            'name': _(self.name),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'hms.estimate',
            'domain': [('patient_id','=',self.id)],
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': {'default_patient_id': self.id},
        }
    
class Hospitalization(models.Model):
    _inherit = "inpatient.registration"
    
    @api.multi
    def action_button_estimation(self):
        return {
            'name': _(self.name),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'hms.estimate',
            'domain': [('inpatient_id','=',self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_inpatient_id': self.id,'default_patient_id': self.patient_id.id,'default_expected_stay': self.expected_stay},
        }

class RoomFacilityCharges(models.Model):
    _name = 'room.facility.charges'

    name = fields.Char('Particulars')
    room_type = fields.Selection([('general', 'General'),('semi_spaecial', 'Semi-Special'),('deluxe', 'Deluxe'),('super_deluxe', 'Super Deluxe'),('suite', 'Suite'),
        ('sharing', 'Sharing'),('icu', 'ICU'),('dialysis', 'Dialysis'),('recovery_room', 'Recovery Room'),], string='Room Type',default='general')
    stay_day = fields.Float('Days')
    room_charges = fields.Float('Charges')
    room_total_amount = fields.Float('Total Amount')
    room_facility_charges_id = fields.Many2one('hms.estimate','Cost Estimaion')

    @api.onchange('stay_day','room_charges')
    def on_room_chanrges(self):
       self.room_total_amount = float(self.stay_day) * float(self.room_charges)


class SurgicalCharges(models.Model):
    _name = 'surgical.charges'

    name = fields.Char('Particulars')
    risk_type = fields.Selection([('high_risk', 'High Risk'),('complicated', 'Complicated'),('emergency','Emeergency')], string='Risk Factor')
    room_type = fields.Selection([('general', 'General'),('semi_spaecial', 'Semi-Special'),('deluxe', 'Deluxe'),('super_deluxe', 'Super Deluxe'),('suite', 'Suite'),
        ('sharing', 'Sharing'),('icu', 'ICU'),('dialysis', 'Dialysis'),('recovery_room', 'Recovery Room'),], string='Room Type',default='general')
    stay_day = fields.Float('Days')
    room_charges = fields.Float('Charges')
    room_total_amount = fields.Float('Total Amount')
    surgical_charges_id = fields.Many2one('hms.estimate','Cost Estimaion')


class OperationEquipCharges(models.Model):
    _name = 'operation.equip.charges'

    name = fields.Char('Particulars')
    room_type = fields.Selection([('general', 'General'),('semi_spaecial', 'Semi-Special'),('deluxe', 'Deluxe'),('super_deluxe', 'Super Deluxe'),('suite', 'Suite'),
        ('sharing', 'Sharing'),('icu', 'ICU'),('dialysis', 'Dialysis'),('recovery_room', 'Recovery Room'),], string='Room Type',default='general')
    stay_day = fields.Float('/Hr & /Mins')
    room_charges = fields.Float('Charges')
    room_total_amount = fields.Float('Total Amount')
    operation_equip_charges_id = fields.Many2one('hms.estimate','Cost Estimaion')

    @api.onchange('stay_day','room_charges')
    def on_operation_chanrges(self):
       self.room_total_amount = float(self.stay_day) * float(self.room_charges)


class InvestigationPharmacyCharges(models.Model):
    _name = 'investigation.pharmacy.charges'

    name = fields.Char('Particulars')
    room_type = fields.Selection([('general', 'General'),('semi_spaecial', 'Semi-Special'),('deluxe', 'Deluxe'),('super_deluxe', 'Super Deluxe'),('suite', 'Suite'),
        ('sharing', 'Sharing'),('icu', 'ICU'),('dialysis', 'Dialysis'),('recovery_room', 'Recovery Room'),], string='Room Type',default='general')
    stay_day = fields.Float('Days')
    room_charges = fields.Float('Charges')
    investigation_pharmacy_charges_id = fields.Many2one('hms.estimate','Cost Estimaion')