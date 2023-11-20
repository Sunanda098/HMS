# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from openerp import api, fields, models

class Product(models.Model):
    _inherit = 'product.template'
    
    hospital_product_type = fields.Selection([
        ('medicament','Medicament'),
        ('prescription','Prescription'),
        ('msupply', 'Medical Supply'),
        ('bed', 'Bed'), 
        ('consultation','Consultation'),
        ('surgery', 'Surgery'), 
        ('procedure', 'Procedure'),
        ('fdrinks', 'Food & Drinks'),
        ('lithotripsy', 'Lithotripsy'),
        ('physiotherapy','Physiotherapy'),
        ('pathology', 'Pathology'), ('radiology', 'Radiology'),
        ('manometry', 'Manometry'),('endoscopy', 'Endoscopy'),
        ('package', 'Insurance Packages'),
        ('charge', 'Patient Charges'),
        ('vaccination','Vaccination'),
#         ('paediatric','Paediatric'),
#         ('orthopedic','Orthopedic'),
        ('os', 'Other Service'),             
#         ('consultation_paediatric','Consultation Paediatric')
        ], string="Hospital Product Type", default='medicament')


class PartnerTPACom(models.Model):
    _inherit = 'res.partner'

    hospital_partner_type = fields.Selection([('tpa', 'TPA'), ('insurance', 'Insurance')], 'Hospital Partner Type')
    claim_reminder = fields.Boolean('Claim Reminder')


class Mediclaim(models.Model):
    _name = 'hms.insurance.mediclaim'

    name = fields.Char('Name')
    active = fields.Boolean('Active')

class Mediclaim(models.Model):
    _name = 'hms.insurance.checklist'

    name = fields.Char('Name')
    active = fields.Boolean('Active')


class RequiredDocuments(models.Model):
    _name = 'hms.insurance.req.doc'
    
    name = fields.Char('Name')
    active = fields.Boolean('Active')


class MediclaimDocType(models.Model):
    _name = 'hms.insurance.mediclaim.doc.type'

    name = fields.Char('Name')
    active = fields.Boolean('Active')


class MediclaimDoc(models.Model):
    _name = 'hms.insurance.mediclaim.doc'


class IpatientOT(models.Model):
    _inherit = 'ot.booking'

    @api.multi
    def create_hospitalization(self):
        inpatient_obj = self.env['inpatient.registration']
        return {
            'name': 'Hospitalization',
            'res_model': 'inpatient.registration',
            'context': {'default_patient_id': self.patient_id.id}
        }


class ZeroErrorBinary(models.Model):
    _name = 'hms.insurance.zero_error.binary'
    _description = 'Zero Error Reporting Images'

    report_image = fields.Binary('Images', required=True)
    zero_error_id = fields.Many2one('hms.insurance.zero_error', 'Zero Error', invisible=True)


class ZeroError(models.Model):
    _name = 'hms.insurance.zero_error'
    _description = 'Zero Error Reporting'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hms.patient', 'Patient', required=True)
    hosp_id = fields.Many2one('inpatient.registration', 'Hospitalization', required=True)
    date_zero_error = fields.Datetime('Date',default=fields.Datetime.now)
    left_right = fields.Char('Left/Right')
    image_one = fields.Binary('Image One')
    image_two = fields.Binary('Image Two')
    image_three = fields.Binary('Image Three')
    image_four = fields.Binary('Image Four')
    image_five = fields.Binary('Image Six')
    image_ids = fields.One2many('hms.insurance.zero_error.binary', 'zero_error_id', 'Images')

class AdmissionCheckList(models.Model):
    _name="hms.inpatient.insurance.checklist"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    inpatient_id = fields.Many2one("inpatient.registration", string="Hospitalization")


class  Attachment(models.Model):
    _inherit = 'ir.attachment'

    patient_id = fields.Many2one('hms.patient', 'Patient')
    hosp_id = fields.Many2one('inpatient.registration', 'Hospitalization')
    req_doc_id = fields.Many2one('hms.insurance.req.doc', 'Doc Type')


class Hospitalization(models.Model):
    _inherit = 'inpatient.registration'

    @api.model
    def _default_insu_checklist(self):
        vals = []
        checklists = self.env['hms.insurance.checklist'].search([('active', '=', True)])
        for checklist in checklists:
            vals.append((0, 0, {
                'name': checklist.name,
            }))
        return vals

    claim_checklist_ids = fields.One2many('hms.inpatient.insurance.checklist', 'inpatient_id', string='Checklist', default=lambda self: self._default_insu_checklist())    

    @api.multi
    def action_patient_doc_view(self):
        res = {
            'name': 'Documents',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'domain': [('res_id', '=', self.patient_id.id), ('res_model', '=', 'hms.patient')],
            'context': {'default_res_id': self.patient_id.id,
                'default_res_model': 'hms.patient',
                'default_patient_id': self.patient_id.id,
                'default_hosp_id': self.id
            },
        }
        return res

    @api.multi
    def action_claim_view(self):
        res = {
            'name': 'Claim',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hms.insurance.claim',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.patient_id.id),('hosp_id','=',self.id)],
            'context': {'default_patient_id': self.patient_id.id,
                'default_hosp_id': self.id
            },
        }
        return res

    @api.multi
    def action_zero_error(self):
        res = {
            'name': '0-0 Error Form',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hms.insurance.zero_error',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.patient_id.id)],
            'context': {'default_patient_id': self.patient_id.id,
                'default_hosp_id': self.id
            },
        }
        return res
    # @api.multi
    # def action_view_invoice_hms(self):
    #     return self.action_create_invoice()

    # @api.multi
    # def action_create_invoice(self):
    #     result = super(Hospitalization,self).action_create_invoice()
    #     invoice_ids = self.env['account.invoice'].search([('report_type', '=', 'claim'), ('partner_id', '=', self.patient_id.partner_id.id)])
    #     imd = self.env['ir.model.data']
    #     action = imd.xmlid_to_object('account.action_invoice_tree1')
    #     list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
    #     form_view_id = imd.xmlid_to_res_id('account.invoice_form')
    #     context = dict(self._context)
    #     context['default_report_type'] = 'inpatient'
    #     context['default_patient_id'] = self.patient_id.id
    #     context['default_hospital_id'] = self.id
    #     context['default_appointment_id'] = self.appointment_id.id
    #     context['default_consultant_doctor_id'] = self.primary_physician.id
    #     context['default_partner_id'] = self.patient_id.partner_id.id
    #     invoice = self.env['account.invoice'].create({
    #                                 'report_type':'inpatient',
    #                                 'patient_id': self.patient_id.id,                     
    #                                 'appointment_id':self.appointment_id.id,
    #                                 'consultant_doctor_id':self.primary_physician.id,
    #                                 'partner_id': self.patient_id.partner_id.id,
    #                                 'hospital_id': self.id,
    #                                             })
    #     self.invoice_id = invoice.id
    #     result = {
    #         'name': action.name,
    #         'help': action.help,
    #         'type': action.type,
    #         'views': [[form_view_id, 'form'], [list_view_id, 'tree'],[False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
    #         'target': action.target,
    #         'res_model': action.res_model,
    #         'res_id': invoice.id,
    #         'domain': [
    #             ('report_type', 'in', ['inpatient']),
    #             ('partner_id', '=', self.patient_id.partner_id.id)
    #         ],
    #         'context': context,
    #     }
    #     return result

#     cashless = fields.Boolean(string="Cashless",default=False)


class Claim(models.Model):
    _name = 'hms.insurance.claim'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'claim_number'
    _description = 'Claim'

    @api.multi
    def _get_diff(self):
        for claim in self:
            claim.amount_difference = claim.amount_requested - claim.amount_pass
            claim.amount_total = claim.amount_received + claim.amount_tds

    claim_number = fields.Char('Claim Number', required=True)
    patient_id = fields.Many2one('hms.patient', 'Patient', required=True)
    hosp_id = fields.Many2one('inpatient.registration', 'Hospitalization',required=True)
    sub_type = fields.Selection([('corporate','Corporate'), ('insurance','Insurance'), ('ppn','PPN')], string='Sub Type', required=True)
    insurance_company_id = fields.Many2one('res.partner', 'Company', domain="[('hospital_partner_type', '=', 'insurance')]")
    policy_number = fields.Char('Policy Number')
    amount_requested = fields.Float('Total Claim Amount')
    amount_pass = fields.Float('Passed Amount')
    amount_received = fields.Float('Received Amount')
    amount_difference = fields.Float(compute='_get_diff', string='Difference Amount')
    amount_tds = fields.Float('TDS Amount')
    amount_total = fields.Float(compute='_get_diff', string='Total Amount')
    date_received = fields.Date('Amount Received Date')
    tpa_id = fields.Many2one('res.partner', 'TPA', domain="[('hospital_partner_type', '=', 'tpa')]", context={'default_hospital_partner_type': 'tpa'})
    req_document_ids = fields.Many2many('hms.insurance.req.doc', 'hms_insurance_req_doc_rel', 'claim_id', 'doc_id', 'Required Documents')
    question = fields.Text('Question')
    answer = fields.Text('Answer')
    #create_date = fields.Datetime(string="Created on Date", default=fields.Datetime.now)
    created_date = fields.Date(string="Created on Date", default=fields.Date.context_today)
    state = fields.Selection([('active', 'Pending'), ('dactive', 'Done')], 'State', default="active")
    invoice_id = fields.Many2one('account.invoice','Account')

    @api.multi
    def action_done(self):
        self.state = 'dactive'

    @api.multi
    def action_create_invoice(self):
        #invoice_ids = self.env['account.invoice'].search([('report_type', '=', 'claim'), ('partner_id', '=', self.patient_id.partner_id.id)])
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')
        invoice = self.env['account.invoice'].create({
                                                    'report_type':'claim',
                                                    'patient_id': self.patient_id.id,                     
                                                    'partner_id': self.patient_id.partner_id.id,
                                                    'appointment_id':self.hosp_id.appointment_id.id,
                                                    'consultant_doctor_id':self.hosp_id.primary_physician.id,
                                                    'treating_doctor_id':self.hosp_id.primary_physician.id,
                                                    'hospital_id': self.hosp_id.id,
                                                    'claim_amout': self.amount_pass,
                                                    'insurance_company_id': self.insurance_company_id.id,
                                                    'tpa_id':self.tpa_id.id,
                                                                })
        self.invoice_id = invoice.id
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[form_view_id, 'form'],[list_view_id, 'tree'],[False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'res_model': action.res_model,
            'res_id': invoice.id,
            'domain': [
                ('report_type', 'in', ['claim']),
                ('partner_id', '=', self.patient_id.partner_id.id)
            ],
            #'context': context,
        }
        return result

    @api.multi
    def action_view_invoice(self):
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
            'domain': [('partner_id','=',self.patient_id.user_id.partner_id.id),('report_type', 'in', ['claim']),('id','=',self.invoice_id.id)],
        }
        if len(invoice_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
        elif len(invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form'), (list_view_id, 'tree')]
            result['res_id'] = invoice_ids.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result


class account_invoice(models.Model):
    _inherit = "account.invoice"


    insurance_company_id = fields.Many2one('res.partner', string='Company')
    tpa_id = fields.Many2one('res.partner', 'TPA', domain="[('hospital_partner_type', '=', 'tpa')]", context={'default_hospital_partner_type': 'tpa'})
    claim_amount = fields.Float(compute='_get_pass_claim_amount', string="Claim Pass Amount")

    
    @api.multi
    def _get_pass_claim_amount(self):
        claim_obj = self.env['hms.insurance.claim']
        for inv in self:
            claims = claim_obj.search([('hosp_id', '=', inv.hospital_id.id)],limit=1)
            inv.insurance_company_id = claims.insurance_company_id.id
            inv.tpa_id = claims.tpa_id.id
            inv.claim_amount = sum([claim.amount_pass for claim in claims])