#-*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models ,_
from openerp.exceptions import UserError
#from duplicity.tempdir import default


class ResCity(models.Model):
    _name = "res.city"

    name = fields.Char('City Name', size=64, required=True)
    state_id = fields.Many2one('res.country.state', 'State', required=True)
    country_id = fields.Many2one(related='state_id.country_id', string='Country')

class ResArea(models.Model):
    _name = "res.area"

    name = fields.Char('Area Name', size=64, required=True)
    city_id = fields.Many2one('res.city', 'City')
    state_id = fields.Many2one(related='city_id.state_id', string='State')
    country_id = fields.Many2one(related='city_id.state_id.country_id', string='Country')
    zip = fields.Char('Zip', size=64)

# class HospitalDepartment(models.Model):
#     _name = "indimedi.hospital.department"
#     _description = "Hospital Department"
# 
#     name = fields.Char('Department', size=64, required=True)


class HospitalDepartment(models.Model):
    _name = "hospital.department"
    _description = "Hospital Department"
    _rec_name = 'name'

    department_name = fields.Selection([('general','General'),('orthopedic', 'Orthopedic'),('paediatric', 'Paediatric'),('cardiology', 'Cardiology'),('gastroenterology', 'Gastroenterology'),('gynaecology', 'Gynaecology')], String="Linked Department")
    name = fields.Char('Department', size=64, required=True)
    active = fields.Boolean("Active", default=True) 

class Insurance(models.Model):
    _name = 'hms.patient.insurance'
    
    insurance_id = fields.Many2one('hms.patient', string ='Insurance Id', ondelete='restrict')
    insurance_company = fields.Char(string ="Insurance Company")
    policy_number = fields.Char(string ="Policy Number")
    insured_value = fields.Float(string ="Insured Value")
    validity = fields.Date(string ="Validity")
    active = fields.Boolean(string ="Active")
    
class RegProduct(models.Model):
    _name = 'hms.patient.reg.product'
    _inherits = {'product.product': 'product_id'}

    product_id = fields.Many2one(
    'product.product', string='Related Product', required=True,
    ondelete='cascade', help='Registration Product')


class ResPartnerPatient(models.Model):
    _inherit = 'res.partner'

    dob = fields.Date(string='Date of Birth')
    sex = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Sex')
    age = fields.Char(string='Age')
    language = fields.Selection([('hindi', 'Hindi'),('english', 'English'),('gujarati', 'Gujarati')], String="Language", default='english')
    marital_status = fields.Selection([('m', 'Married'),
                            ('u', 'Unmarried'),
                            ('w', 'Widowed'),
                            ('d', 'Divorced'),
                            ('x', 'Separated'),
                            ('z', 'Live In Relationship'),
                            ('s', 'Single'),
                            ],
                           string='Marital Status', sort=False)

class IndiPatient(models.Model):
    _name = 'hms.patient'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherits = {
        'res.users': 'user_id',
    }
    _description = 'Patient'
    _order = 'create_date desc'
    
#Block Code Shah Hospital 0n Feb14
    # @api.model
    # def _get_default_dr(self):
    #     dr_id = self.env['hms.physician'].search([('name','ilike','Dr. Manish Shah')],limit=1)
    #     if dr_id:
    #         return dr_id[0]
    #     else:
    #         return False

    @api.model
    def _get_department(self):
        dept = self.env['hospital.department'].search([('department_name','=','gastroenterology')],limit=1)
        if dept:
            return dept[0]
        else:
            return False

    old_id = fields.Integer('Old ID')
    code = fields.Char(size=256, string='Patient ID', help='Patient Identifier provided by the Health Center.Is not the Social Security Number')
    gov_code = fields.Char(string='Aadhar No.')
    active = fields.Boolean(string='Active', help="If unchecked, it will allow you to hide the patient without removing it.",default=True)
    product_id = fields.Many2one('product.product', 'Product', ondelete='restrict')
    invoice_id = fields.Many2one('account.invoice',string='Invoice', ondelete='restrict')
    total_invoiced = fields.Float(compute="_invoice_total", string="Total Invoiced",groups='base.group_user,account.group_account_invoice')
    is_corpo_tieup = fields.Boolean(string='Corporate Tie-Up', help="If not checked, these Corporate Tie-Up Group will not be visible at all.")
    company_id = fields.Many2one('res.partner', string='Company', domain="[('is_company', '=', True),('customer', '=', True)]", ondelete='restrict')
    emp_code = fields.Char(string='Employee ID')
    insurance_ids = fields.One2many('hms.patient.insurance','insurance_id',string='Insurance')
    state = fields.Selection([('draft',"Draft"),('invoiced',"invoiced")],string="Status",default='draft')
    user_id = fields.Many2one(
    'res.users', string='Related User', required=True,
    ondelete='cascade', help='User-related data of the patient',store=True)
    primary_doctor = fields.Many2one('hms.physician', 'Primary Care Doctor', ondelete='restrict')
    ref_doctor = fields.Many2many('referring.doctors','rel_doc_pat','doc_id','patient_id', 'Referring Doctors')
    refer_type1 = fields.Selection([('advertisement','Advertisement'),('camp','Camp'),('employee','Employee'),('friend','Friend'),('patient','Patient'),('ref. Dr.','Ref. Dr.'),('relative','Relative'),('self','Self'),('website','Website'),], string='Referred Type')
    #For Basic Medical Info
    blood_group = fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')], string='Blood Group')
    critical_info = fields.Text(string='Important disease, allergy or procedures information', help='Write any important information on the patient\'s disease, surgeries, allergies, ...')
    #Diseases
    medical_history = fields.Text(string="Past Medical History")
    patient_diseases = fields.One2many('hms.patient.disease', 'patient_id', string='Diseases', help='Mark if the patient has died')
    #Family Form Tab
    genetic_risks = fields.One2many('hms.patient.genetic.risk', 'patient_id', 'Genetic Risks')
    family_history = fields.One2many('hms.patient.family.diseases', 'patient_id', 'Family History')
    department_id = fields.Many2one('hospital.department', 'Department', default=_get_department)
    #language selection
    language = fields.Selection([('hindi', 'Hindi'),('english', 'English'),('gujarati', 'Gujarati')], String="Language", default='english')
    area_id = fields.Many2one('res.area', 'Area')
    city_id = fields.Many2one('res.city', 'City')
    findings = fields.Text('Findings')
    visits = fields.Integer('Visits')
    sex = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Sex')
    weight = fields.Float('Weight(kg)')
    feet = fields.Float('Height(feet)',default=0)
    inch = fields.Float('Height(inch)',default=0)
    cm = fields.Float('Height(cm)', digits=(16,2))
    # bmi = fields.Float('BMI',compute="_get_bmi",digits=(16,2),store=False)
    occupation = fields.Char(string='Occupation')
    # clinical_research = fields.Boolean(string='Clinical Research')
    pan_no = fields.Char('PAN No')
    bmi_line_ids = fields.One2many('bmi.records','patient_id', string="BMI Records")

#     @api.depends('feet','inch')
#     def _get_height(self):
#         self.cm = ((float(self.feet) * 12) + float(self.inch)) * 2.54
# 
#     @api.onchange('feet','inch')
#     def onchange_feet(self):
#         self.cm = ((float(self.feet) * 12) + float(self.inch)) * 2.54

    # @api.depends('cm','weight')
    # def _get_bmi(self):
    #     if self.cm:
    #         self.bmi = round((float(self.weight) / ((float(self.cm) / 100) ** 2)),2)

    # @api.model
    # def create(self, values):
    #     if not self._context.get('online'): 
    #         if values.get('old_id', ''):
    #             old_id = values.get('old_id', '')
    #             old = self.search([('old_id', '=', old_id)])
    #             if old:
    #                 return old
    #         if values.get('mobile', ''):
    #             mobile = values.get('mobile', '')
    #             loging = self.search([('login', '=', mobile)])
    #             if not loging:
    #                 values['login'] = values.get('mobile', '')
    #     if values.get('code', '') == '':
    #         values['code'] = self.env['ir.sequence'].next_by_code('hms.patient') or ''
    #         #values['login'] = values['code']
    #     values['customer'] = True
    #     values['groups_id'] = []
    #     res = super(IndiPatient, self).create(values)
    #     if not values.get('password'):
    #         res.user_id.write({'password':values.get('login')})
    #     group_user = self.env.ref('hms.group_hms_user')
    #     res.write({'groups_id': [(6, 0, [group_user.id])]})
    #     return res


    @api.model
    def create(self, values):
        mobile = values.get('mobile', '')
        if mobile:
            loging = self.env['res.users'].search([('login', '=', str(mobile))])
            if not loging:
                values['login'] = mobile
        if values.get('code', '') == '':
            values['code'] = self.env['ir.sequence'].next_by_code('hms.patient') or ''
        values['password'] = values['login'] = values.get('login', None) or values['code']
        values['customer'] = True
        values['groups_id'] = []
        res = super(IndiPatient, self).create(values)
        group_user = self.env.ref('hms.group_hms_user')
        res.write({'groups_id': [(6, 0, [group_user.id])]})
        return res

    @api.multi
    def toggle_active(self):
        """ Inverse the value of the field ``active`` on the records in ``self``. """
        for record in self:
            record.active = not record.active

    @api.onchange('city_id')
    def onchange_city(self):
        if self.city_id:
            self.state_id = self.city_id.state_id.id or False
            self.city = self.city_id.name

    @api.onchange('login')
    def onchange_login(self):
        if self.login and len(self.login) >= 10:
            self.mobile = self.login

    @api.onchange('area_id')
    def onchange_area(self):
        if self.area_id:
            self.city_id = self.area_id.city_id.id or False
            self.state_id = self.area_id.city_id.state_id.id
            self.city = self.area_id.city_id.name
            self.zip = self.area_id.zip
            self.country_id = self.area_id.city_id.state_id.country_id.id


    @api.multi
    @api.onchange('state_id')
    def onchange_state(self):
        if not self.state_id:
            return {'value': {}}
        self.country_id = self.state_id.country_id.id
       
    @api.multi
    def invoiced_create_state(self):
        return self.write({'state':'invoiced'})

    @api.onchange('dob')
    def onchange_dob(self):
        if self.dob:
            b_date = datetime.strptime(self.dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (delta.years, delta.months, delta.days)
            else:
                age = _("%syear") % (delta.years)
            self.age = age
            if delta.days < 0 :
                raise UserError(('You cannot enter Future DATE OF BIRTH'))


    @api.multi
    def create_invoice(self):
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']
        reg_product = self.env['hms.patient.reg.product'].search([], limit=1)
        if not reg_product:
            UserError(('Please first configure patient registration fee in configuration.'))
        account_id = False
        if reg_product.product_id.id:
            account_id = reg_product.product_id.property_account_income_id.id
        if not account_id:
            prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
            account_id = prop and prop.id or False
        invoice = inv_obj.create({
            'name': '-',
            'account_id': self.partner_id.property_account_receivable_id.id,
            'partner_id': self.partner_id.id,
            'patient_id': self.id,
            'origin': self.code,
            'type': 'out_invoice',
            'currency_id': self.env.user.company_id.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': reg_product.product_id.name,
                'price_unit': reg_product.product_id.lst_price,
                'account_id': account_id,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': reg_product.product_id.uom_id.id,
                'product_id': reg_product.product_id.id,
                'account_analytic_id': False,
                'invoice_line_tax_ids': [(6, 0, [x.id for x in reg_product.taxes_id])]
            })],
        })
        return self.write({'state': 'invoiced', 'invoice_id': invoice.id})

    @api.multi
    def view_invoice(self):
        invoice_ids = self.mapped('invoice_id')
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'domain': [('partner_id','=',self.user_id.partner_id.id)],
        }
        if len(invoice_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
        elif len(invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form'), (list_view_id, 'tree')]
            result['res_id'] = invoice_ids.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    @api.multi
    def action_appointment(self):
        return {
            'name': _('Appointments'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'hms.appointment',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id','=',self.id)],
            'context': {
                        'default_patient_id': self.id,
                        'default_physician_id':self.primary_doctor.id,
                        'default_urgency':'a',
                        'default_department_id':self.department_id.id,
                        #'default_ref_doctor':self.ref_doctor[0].id,
                        },
        }

class BMIRecord(models.Model):
    _name = 'bmi.records'

    patient_id = fields.Many2one('hms.patient', string="Patient")
    bmi_date = fields.Date(string="Date", default=datetime.now())
    weight = fields.Float('Weight(kg)')
    cm = fields.Float('Height(cm)', digits=(16,2))
    bmi = fields.Float('BMI',compute="_get_bmi",digits=(16,2))

    @api.depends('cm','weight')
    def _get_bmi(self):
        for rec in self:
            if rec.cm:
                rec.bmi = round((float(rec.weight) / ((float(rec.cm) / 100) ** 2)),2)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
