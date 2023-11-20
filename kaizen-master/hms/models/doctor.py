# -*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _
from openerp.exceptions import UserError
from openerp.tools import amount_to_text_en, float_round
from openerp import SUPERUSER_ID, models
import openerp

class ResUsers(models.Model):
    _inherit= "res.users"

    department_ids = fields.Many2many('hospital.department', 'user_department_rel', 'user_id','department_id', string='Departments')


class PhysicianSpecialty(models.Model):
    _name = 'physician.specialty'

    code = fields.Char(size=256, string='Code')
    name = fields.Char(size=256, string='Speciality', required=True,translate=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]


class PhysicianDegree(models.Model):
    _name = 'physician.degree'

    name = fields.Char(string='Degree')


class Physician(models.Model):
    _name = 'hms.physician'
    _inherits = {
        'res.users': 'user_id',
    }

    user_id = fields.Many2one('res.users',string='Related User',required=True,
        ondelete='cascade', help='User-related data of the physician')
    code = fields.Char(size=256, string='ID')
    degree_ids = fields.Many2many('physician.degree', 'physician_rel_education', 'physician_ids','degree_ids', string='Tags')
    specialty = fields.Many2one('physician.specialty', ondelete='set null', string='Speciality', help='Specialty Code')
    active = fields.Boolean(string='Active', help="If unchecked, it will allow you to hide the physician without removing it.", default=True)
    government_id = fields.Char(string='Government ID')
    website = fields.Char(string='Website')
    patient_id = fields.Many2one('hms.patient',ondelete='restrict', string='Patient')
    consul_service = fields.Many2one('product.product', ondelete='restrict', string='Consultation Service')
    consul_charge = fields.Integer('Consultation Charge')
    is_primary_surgeon = fields.Boolean(string='Primary Surgeon')
    is_consultation_doctor = fields.Boolean(string='Consultation Doctor')
    signature = fields.Binary('Signature')
    department_ids = fields.Many2many('hospital.department', 'physician_department_rel', 'physician_id','department_id', string='Departments')
    reg_number = fields.Char(string='Reg. No.')
    cabin_no = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')], string='Cabin')
    type = fields.Selection([('standard','Standard'),('outside','Outside'),('specialist','Specialist')],string="Type")
    special_ids = fields.One2many('hms.special.service', 'doctor_id', string="Special Services")
    designation= fields.Char(string='Designation',)
    highest_qualification_id= fields.Many2one('physician.degree',string='Highest Qualification')
    relation = fields.Char(string='Husband of /Wife of')
    age = fields.Char(string='Age')
    
    @api.model
    def create(self, values):
        if values.get('code', '') == '':
            values['code'] = self.env['ir.sequence'].next_by_code('hms.physician')
        res = super(Physician, self).create(values)
        return res

    # @api.multi
    # def amount_to_text(self, amount, currency='INR'):
    #     print (">>>>>>>>>>>>>>>",self)
    #     return amount_to_text(self.consul_charge, lang='en_IN', currency='INR')

    # amount_to_text_en.amount_to_text(math.floor(self.amount), lang='en', currency='')

# <span t-esc="o.amount_to_text(o.amount_total, 'Euro')"/> 

    @api.multi
    def test_amount_to_text(self):
        print (">>>>>>>>>>>>>>>>>>>>>>>>>>>",)
        word_1=amount_to_text_en.amount_to_text(self.consul_charge,lang='en_IN', currency='Rupees')
        check_amount_in_words = word_1.replace(' and Zero Cent', '')
        return [{'amount_text':check_amount_in_words}]
    # @api.multi
    # def test_amount_to_text(self):
    #     result = {}
    #     list_data = []
    #     result = {'amount_text': self.currency_id.amount_to_text(
    #         round(self.amount_total))}
    #     list_data.append(result)
    #     return list_data

class SpecialServices(models.Model):
    _name = 'hms.special.service'
    
    product_id = fields.Many2one('product.product', string="Service")
    hospital_share = fields.Float('Hospital Share')
    ksga_share = fields.Float('KSGA Share')
    amount = fields.Float('Amount')
    doctor_id = fields.Many2one('hms.physician',string="Doctor")
    
class ReferringDoctors(models.Model):
    _name = 'referring.doctors'

    name = fields.Char('Name')
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    mobile = fields.Char('Mobile')
    address = fields.Char('Address')
    country = fields.Char('City')
    city = fields.Char('Country')
    refer_type1 = fields.Selection([('advertisement','Advertisement'),('camp','Camp'),('employee','Employee'),('friend','Friend'),('patient','Patient'),('ref. Dr.','Ref. Dr.'),('relative','Relative'),('self','Self'),('website','Website'),], string='Referred Type')
    state_ref = fields.Char('State')
    
# class ReferringDoctorsType(models.Model):
#     _name = 'referring.type'

#     name = fields.Char('Name')
#     ref_by = fields.One2many('referring.doctors', 'refer_type',string='ref by')