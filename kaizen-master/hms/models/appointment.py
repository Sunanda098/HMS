# -*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _
from openerp.exceptions import UserError

class ComplainLine(models.Model):
    _name = 'hms.appointment.chief.complain.line'

    name= fields.Char('Name')

class ChiefComplain(models.Model):
    _name = 'hms.appointment.chief.complain'

    name = fields.Many2one('hms.appointment.chief.complain.line', 'Name')
    days = fields.Float('Day')
    appointment_id = fields.Many2one('hms.appointment', 'Appointment Id', ondelete='cascade')


class AppFinding(models.Model):
    _name = 'hms.appointment.finding'
    name = fields.Char('Name')


class Finding(models.Model):
    _name = "opd.finding"

    name = fields.Many2one('hms.appointment.finding', 'Name')
    description = fields.Char('Description')
    datetime = fields.Datetime('Date', default=fields.Datetime.now)
    appointment_id = fields.Many2one('hms.appointment', 'Appointment', ondelete='cascade')


class AppointmentPurpose(models.Model):
    _name = 'appointment.purpose'

    name = fields.Char(size=256, string='Appointment Purpose', required=True, translate=True)
    product_id = fields.Many2one('product.product', string="Product")


class Appointment(models.Model):
    _name = 'hms.appointment'
    _order= 'date_start desc'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def _get_service_id(self):
        return self.product_id.search([('hospital_product_type', '=', 'consultation')], limit=1).id

    @api.model
    def _get_reason_id(self):
        return self.env.ref("hms.reason_routine_follow")

    @api.model
    def _get_purpose_id(self):
        return self.env.ref("hms.purpose_consultation")

    @api.multi
    def _time_count(self):
        # pass
       for rec in self:
           date_end = datetime.strptime(rec.date_end, '%Y-%m-%d %H:%M:%S') if rec.date_end else  datetime.now()
           if rec.date_start:
               datetime_diff = date_end - datetime.strptime(rec.date_start, '%Y-%m-%d %H:%M:%S')
               hrs = datetime_diff.seconds / 3600
               mins = datetime_diff.seconds % 3600 / 60
               if mins in range(1,10):
                   rec.waiting_duration = "%s:0%s" % (hrs, mins)
               else:
                   rec.waiting_duration = "%s:%s" % (hrs, mins)
               sec  = datetime_diff.seconds % 60
           else:
               rec.waiting_duration = "0:0"
                
    name = fields.Char(size=256, string='Appointment Id', readonly=True,default='New Appointment', copy=False, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    patient_id = fields.Many2one('hms.patient', ondelete='restrict',  string='Patient',required=True, select=True,help='Patient Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    image = fields.Binary(related='patient_id.image',string='Image', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    physician_id = fields.Many2one(related="patient_id.primary_doctor", ondelete='restrict', string='Doctor', select=True,help='Physician\'s Name', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, required=True)
    department_id = fields.Many2one('hospital.department', 'Department', ondelete='restrict')
    no_invoice = fields.Boolean(string='Invoice Exempt', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    date = fields.Datetime(string='Date', default=fields.Datetime.now, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    urine_reports = fields.Char(string='Urine Reports', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    s_creatinine = fields.Char(string='S.Creatinine', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    bi_sugar = fields.Char(string='BI.Sugar', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    cbc = fields.Char(string='CBC', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    blood_group = fields.Char(string='Blood Group', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    spsa = fields.Char(string='SPSA', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    electrolytes = fields.Char(string='Electrolytes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    others = fields.Char(string='Others', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    usg_abdomen_kub = fields.Char(string='USG Abdomen/KUB', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    x_ray_kub = fields.Char(string='X-Ray/KUB', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    rgu = fields.Char(string='RGU', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    mcu = fields.Char(string='MCU', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    ct_scan = fields.Char(string='C.T. Scan', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    renal_scan = fields.Char(string='Renal Scan', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    bone_scan = fields.Char(string='Bone Scan', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    otherss = fields.Char(string='Others', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    reason_id = fields.Many2one("hms.reason",ondelete='set null', string="Reason", states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, default=_get_reason_id)
    follow_date = fields.Datetime(string="Follow Up Date", states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    weight = fields.Float(string='Weight', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    temp = fields.Char(string='Temp', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    hr = fields.Char(string='HR', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})

    # rr = fields.Char(string='RR', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # bp = fields.Char(string='BP', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # spo2 = fields.Char(string='SpO2', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})

    differencial_diagnosis = fields.Text(string='Differencial Diagnosis', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    medical_advice = fields.Text(string='Medical Advice', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    #Below Fields Copy from Shah opd
    complain_ids = fields.Many2many('chief.complain','appointment_rel_complain','appointment_id','complain_ids' , string='Chief Complain')
    complain_ids_dummy = fields.Many2many('chief.complain','appointment_rel_complain_dummy','appointment_id','complain_ids' , string='Chief Complain')
    chief_complain = fields.Text(string='Chief Complaints', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    present_illness = fields.Text(string='History of Present Illness', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    notes = fields.Text(string='Notes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    rs = fields.Text(string='Respiratory Syncytial', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    cvs = fields.Text(string='C.V.S.', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    cns = fields.Text(string='C.N.S', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    per_abdominal = fields.Text(string=' Per Abdominal', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    per_rectal = fields.Text(string='Per Rectal Examination', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    per_vaginal = fields.Text(string='Per Vaginal Examination', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    external_genitals = fields.Text(string='External Genitals', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    back_spine = fields.Text(string='Back Spine', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # peripheral_pulsation = fields.Text(string='Peripheral Pulsation', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    notess = fields.Text(string='Notes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    advice_notes = fields.Text(string='Notes', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    past_ho = fields.Text('Past H/O')
    associated_disease = fields.Many2one('hms.diseases','Disease and Description"')
    associated_diseases = fields.One2many('associated.diseases','associated_diseases_id',string='Disease and Description')
    post_medication = fields.Text('Past Medication')
    previous_inv = fields.Text('Present Medication')
    family_ho = fields.Text('Family H/O')
    past_history = fields.Text(string='Past History', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    comments = fields.Text(string='Comments', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    invoice_id = fields.Many2one('account.invoice', string='Invoice', ondelete='cascade', copy=False)
    urgency = fields.Selection([
        ('a', 'Normal'),
        ('b', 'Urgent'),
        ('c', 'Medical Emergency'),
    ], string='Urgency Level', default='a', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('waiting', 'Waiting'),
        ('in_consultation', 'In consultation'),
        ('invoiced', 'Invoiced'),
        ('invoice_exempt', 'Invoice Exempt'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='State',default='draft', required=True, copy=False, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    product_id = fields.Many2one('product.product', ondelete='restrict', string='Consultation Service', help="Consultation Services", domain=[('hospital_product_type', 'in', ("consultation"))], required=True, default=_get_service_id, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    age =  fields.Char(related='patient_id.age', string='Age', readonly=True)
    company_id = fields.Many2one('res.company', ondelete='restrict', string='Institution',default=lambda self: self.env.user.company_id.id, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})  #search lambda for company
    duration = fields.Float(string='Duration', default=15.00, states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    no_invoice = fields.Boolean('Invoice Exempt', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    consultation_type = fields.Selection([('consultation','Consultation'),('followup','Follow Up')],'Consultation Type', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    #Diseases
    medical_history = fields.Text(related='patient_id.medical_history',string="Past Medical History")
    patient_diseases = fields.One2many('hms.patient.disease', related='patient_id.patient_diseases', string='Diseases', help='Mark if the patient has died', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    date_start = fields.Datetime('Waiting Start Date', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    date_end = fields.Datetime('Waiting end Date', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    waiting_duration = fields.Char('Wait Time', compute="_time_count" ,readonly=True)
    purpose_id = fields.Many2one('appointment.purpose',ondelete='cascade', string='Purpose', help="Appointment Purpose", states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, default=_get_purpose_id, required=True)
    days_1 = fields.Integer(string='Days', default=15,states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    weeks = fields.Integer(string='Weeks', default=0,states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    months = fields.Integer(string='Months', default=0,states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    area_id = fields.Many2one(related='patient_id.area_id',string='Area')
    sequence = fields.Integer(help='Used to order Appointment in tree view' ,default=10)
    state_id = fields.Many2one(related="patient_id.state_id", string="State")

    @api.onchange('complain_ids')
    def onchange_complain_ids(self):
        complain = (self.complain_ids - self.complain_ids_dummy)
        if complain and self.chief_complain:
            self.chief_complain += str("\n" + complain.name)
        elif complain and not self.chief_complain:
            self.chief_complain = complain.name
        self.complain_ids_dummy = self.complain_ids
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.patient_id and record.patient_id.name:
                name += ' - ' + record.patient_id.name
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|',('name',operator,name),('patient_id.name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.model
    def create(self, values):
        if values.get('name', 'New Appointment') == 'New Appointment':
            values['name'] = self.env['ir.sequence'].next_by_code('hms.appointment') or 'New Appointment'
        return super(Appointment, self).create(values)

    @api.multi
    def unlink(self):
        for data in self:
            if data.state in ['done']:
                raise UserError(('You can not delete record in done state'))
        return super(Appointment, self).unlink()

    @api.multi
    def create_invoice(self):
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']
        inv_line_obj = self.env['account.invoice.line']
        account_id =  False
        if self.product_id.id:
            account_id = self.product_id.property_account_income_id.id
        if not account_id:
            prop = ir_property_obj.get('property_account_income_categ_id', 'product.category')
            account_id = prop and prop.id or False
        invoice = inv_obj.create({
            'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
            'partner_id': self.patient_id.partner_id.id,
            'patient_id': self.patient_id.id,
            # 'patient_clinical_research':self.patient_id.clinical_research,
            'type': 'out_invoice',
            'name': '-',
            'origin': self.name,
            'report_type':'consult',
            'appointment_id': self.id,
            'consultant_doctor_id':self.patient_id.primary_doctor.id,
            'treating_doctor_id':self.patient_id.primary_doctor.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.product_id.name,
                'price_unit': self.product_id.lst_price,
                'account_id': account_id,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': self.product_id.uom_id.id,
                'product_id': self.product_id.id,
                'account_analytic_id': False,
            })],
        })
        #self.state = 'invoiced'
        self.invoice_id = invoice.id

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
            'id': action.id,
            'domain': [('partner_id','=',self.patient_id.user_id.partner_id.id),('appointment_id','=',self.id)],
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
    def button_refering_dr(self):
        return {
            'name': _('Referring Dr.'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'hms.appointment',
            'type': 'ir.actions.act_window',
            'domain': [('physician_id','=',self.physician_id.id)],
            'context': {'default_physician_id': self.physician_id.id,'default_patient_id': self.patient_id.id},                        
        }

 #fixed onchange on product    
    @api.depends('patient_id')
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        appointment_id = self.search([('patient_id','=',self.patient_id.id)])
        self.physician_id = self.patient_id.primary_doctor.id
        self.department_id = self.patient_id.department_id.id
        if appointment_id:
            self.consultation_type='followup'
        else:
            self.consultation_type = 'consultation'

    @api.depends('physician_id')
    @api.onchange('physician_id')
    def onchange_doctor(self):
        print "[=======ehe==========="
        if self.physician_id:
            self.product_id = self.physician_id.consul_service.id or False

    @api.multi
    def action_list_appointment(self):
        return {'view_type': 'form' ,'view_mode': 'tree,form','type': 'ir.actions.client', 'tag': 'history_back'}

    @api.multi
    def appointment_done(self):
        self.state = 'done'
        self.date_end = datetime.now()
        return self.action_list_appointment()

    @api.multi
    def appointment_confirm(self):        
        self.state = 'confirm'

    @api.one
    def appointment_waiting(self):
        self.state = 'waiting'
        self.sequence = 1
        self.date_start = datetime.now()

    @api.one
    def appointment_consultation(self):
        self.state = 'in_consultation'
        self.date_end = datetime.now()
        self.sequence = 2

    @api.one
    def appointment_draft(self):
        self.state = 'draft'

class OemedicalReason(models.Model):
    _name= "hms.reason"
    
    name = fields.Char(string="Reason")

class AssociatedDiseasess(models.Model):
    _name = "associated.diseases"

    associated_diseases_name = fields.Many2one('hms.diseases','Disease')
    associated_diseases_desc = fields.Char(string='Description')
    associated_diseases_id = fields.Many2one('hms.appointment','Disease')

#### THIS CLASS COPY FROM SHAH OPD ###

class ChiefComplains(models.Model):
    _name = 'chief.complain'

    name = fields.Char('Chief Complain')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
