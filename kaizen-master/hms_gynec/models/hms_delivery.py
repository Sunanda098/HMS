# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class Delivery(models.Model):
    _name = "hms.delivery"
    _description = "Delivery"

    @api.multi
    def _address(self):
        result = {}
        for rec in self:
            if rec.hospitalizaion_id:
                result[rec.id] = ((str(rec.hospitalizaion_id.patient_id.street + ',')) if rec.hospitalizaion_id.patient_id.street else '' ) \
                + ((str(rec.hospitalizaion_id.patient_id.street2 + ','))  if rec.hospitalizaion_id.patient_id.street2 else '' ) \
                + ((str(rec.hospitalizaion_id.patient_id.city + ',')) if rec.hospitalizaion_id.patient_id.city else '' ) \
                + ((str(rec.hospitalizaion_id.patient_id.state_id.name + ',')) if rec.hospitalizaion_id.patient_id.state_id else '' ) \
                + ((str(rec.hospitalizaion_id.patient_id.zip + ',')) if rec.hospitalizaion_id.patient_id.zip else '' ) \
                + ((str(rec.hospitalizaion_id.patient_id.country_id.name)) if rec.hospitalizaion_id.patient_id.country_id else '')
        return result

    @api.multi
    def _blood_group(self):
        result = {}
        for rec in self:
            if rec.hospitalizaion_id:
                result[rec.id] = rec.hospitalizaion_id.patient_id.blood_group
        return result

    @api.multi
    def write(self,vals):
        patient_obj = self.env['hms.patient']
        vals['parity'] = self.patient_id.n_nb_male + self.patient_id.s_nb_male + self.patient_id.n_nb_female + self.patient_id.s_nb_female
        vals['male'] = self.patient_id.n_nb_male + self.patient_id.s_nb_male 
        vals['female'] = self.patient_id.n_nb_female + self.patient_id.s_nb_female
        super(Delivery, self).write(vals)
        return True

    @api.onchange('hospitalizaion_id')   
    def onchange_hospitalizaion(self):
        res = {'value':{}}
        if self.hospitalizaion_id:
            self.patient_id = self.hospitalizaion_id.patient_id.id

    name = fields.Char('Name of Children')
    hospitalizaion_id = fields.Many2one('inpatient.registration', string='Hospitalization')
    patient_id = fields.Many2one('hms.patient', string="Mother Name")
    age = fields.Char(related='patient_id.age',string="Age", readonly=1)
    husband_name = fields.Char(related='patient_id.husband_name', string="Husband's Name", readonly=1)
    husband_edu = fields.Char(related='patient_id.husband_edu',string="Husband's Education", readonly=1)
    husband_business = fields.Char(related='patient_id.husband_business',string="Husband's Business", readonly=1)
    patient_education = fields.Char(related='patient_id.education',string="Patient Education", readonly=1)
    hb = fields.Float(related='patient_id.hb',string="HB", readonly=1)
    blood_group = fields.Char(compute=_blood_group, string="Blood Group", readonly=1)
    patient_address = fields.Char(compute=_address, string="Address", readonly=1)
    parity = fields.Integer(string="Parity", readonly=1)
    male = fields.Integer(string="M", readonly=1)
    female = fields.Integer(string="F", readonly=1)
    delivery_type = fields.Selection ([
            ('normal', 'Normal'),
            ('cesarean', 'Cesarean'),
            ], string='Type of Delivery')
    sex = fields.Selection ([
            ('male','Male'),
            ('female','Female'),
            ], string='Sex', select=True)
    dob = fields.Date(string='Date of birth')
    tob = fields.Char(string='Time of birth')
    birth_weight = fields.Float(string='Birth Weight')
    extra_info = fields.Text (string='Remarks')
    state = fields.Selection([('draft', 'Draft'),('done', 'Done')],
    string='Status', required=True, readonly=True, copy=False,default='draft')


    @api.multi
    def set_delivery_state_done(self):
        self.state = 'done'

class IndimediPatient(models.Model):
    _inherit = "hms.patient"

    delivery_ids = fields.One2many('hms.delivery', 'patient_id',string='Delivery')
    nb_male= fields.Integer(string='No of male',default=0)
    n_nb_male = fields.Integer(string='N-M',default=0)
    s_nb_male = fields.Integer(string='S-M',default=0)
    nb_female = fields.Integer(string='No of female',default=0)
    n_nb_female = fields.Integer(string='N-F',default=0)
    s_nb_female = fields.Integer(string='S-F',default=0)
    
    @api.multi
    def action_view_patient_delivery(self):
        return {
            'name': _('Patient Deliveries'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hms.delivery',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id','=',self.id)],
        }

class IndimediInpatientRegistration(models.Model):
    _inherit = "inpatient.registration"
    
    delivery_ids = fields.One2many('hms.delivery', 'hospitalizaion_id',string='Delivery')
    
    @api.multi
    def action_view_patient_delivery(self):
        return {
            'name': _('Patient Deliveries'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hms.delivery',
            'type': 'ir.actions.act_window',
            'domain': [('hospitalizaion_id','=',self.id)],
        }
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
        
