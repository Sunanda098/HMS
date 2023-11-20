# -*- coding: utf-8 -*-

from openerp import api, fields, models, exceptions, _
from datetime import datetime,date
import time


class IndimediProcedure(models.Model):
    _name = 'medical.procedure'
    _description = 'Medical Procedure'
    _inherit = 'mail.thread'
    _rec_name = 'seq_name'


    app_id = fields.Many2one('hms.appointment', string='Appointment')
    state = fields.Selection([('draft',"Draft"),('in_progress',"In Progress"),('done',"Done"), ('invoiced', 'Invoiced')],string="Status",default='draft')
    seq_name = fields.Char(string="Medical Procedure #", readonly='1')
    patient_id = fields.Many2one("hms.patient",string="Patient", required=True)
    doctor_id = fields.Many2one("hms.physician",string="Doctor", required=True)
    ref_doctor_id = fields.Many2one('referring.doctors',string='Referring Doctor')
    create_date = fields.Datetime(string="Creation Date ", required=True,default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    end_date = fields.Datetime(string='Procedure Date')
    procedure_type = fields.Many2one("procedure.type",string="Procedure Type", required=True)
    hospitalization = fields.Many2one('inpatient.registration',string='Hospitalization')
    invoice_status = fields.Selection([('invoiced','Invoiced'),('tobe','To be Invoiced'),('no','No Invoice')],string='Invoice Status')
    invoice_id = fields.Many2one('account.invoice',string='Invoice')
    diagnosis = fields.Text(string='Diagnosis')
    procedure = fields.Text(string='Procedure')
    advice = fields.Text(string='Advices')

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'draft':
            return 'hms_medical_procedure.mt_alert_medical_procedure_draft'
        elif 'state' in init_values and self.state == 'in_progress':
            return 'hms_medical_procedure.mt_alert_medical_procedure_in'
        elif 'state' in init_values and self.state == 'done':
            return 'hms_medical_procedure.mt_alert_medical_procedure_done'
        return super(IndimediProcedure, self)._track_subtype(init_values)

    @api.onchange('patient_id')
    def get_hospitalization(self):
        hosp_ids = self.env['inpatient.registration'].search([('patient_id', '=', self.patient_id.id)])
        if hosp_ids:
            self.hospitalization = hosp_ids[0].id

    @api.multi
    def create_invoice(self):
        for order_id in self:
            if order_id.procedure_type.product_id.id:
                account_id = order_id.procedure_type.product_id.property_account_income_id.id
            if not account_id:
                prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
                account_id = prop and prop.id or False
            inv_id = self.env['account.invoice'].create({
                'account_id': order_id.patient_id.partner_id.property_account_receivable_id.id,
                'partner_id': order_id.patient_id.partner_id.id,
                'patient_id': order_id.patient_id.id,
                'consultant_doctor_id': order_id.doctor_id.id,
                'treating_doctor_id': order_id.doctor_id.id,
                'date_invoice': fields.date.today(),
                'origin': self.seq_name,
                'report_type' : 'procedure',
                'invoice_line_ids': [(0, 0, {
                    'product_id': order_id.procedure_type.product_id.id,
                    'name':  order_id.procedure_type.product_id.name,
                    'price_unit': order_id.procedure_type.product_id.lst_price,
                    'invoice_id': inv_id.id,
                    'account_id': account_id,
                })],
            })
            order_id.invoice_id = inv_id.id
            order_id.state = invoiced

    @api.multi
    def action_view_invoice(self):
        mod_obj = self.env['ir.model.data']
        result = mod_obj.get_object('account', 'action_invoice_tree1')
        result = result.read()[0]
        #compute the number of invoices to display
        inv_ids = [rec.invoice_id.id for rec in self]
        #choose the view_mode accordingly
        if len(inv_ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, inv_ids))+"])]"
        else:
            res = mod_obj.get_object('account', 'invoice_form')
            result['views'] = [(res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result

    @api.multi
    def button_inprogress(self):
        self.seq_name = self.env['ir.sequence'].next_by_code('medical.procedure')
        self.state = 'in_progress'

    @api.multi
    def button_done(self):
        self.state = 'done'

    @api.multi
    def unlink(self):
        if any([x and x != 'draft' for x in self.mapped('state')]):
            raise exceptions.Warning(_('OPP can be delete only in Draft state'))
        return super(IndimediProcedure, self).unlink()

class Proceduretype(models.Model):
    _name = 'procedure.type'
    _description = 'Medical Procedure Type'

    name = fields.Char(string="Name", required= True)
    product_id = fields.Many2one("product.product",string="Service", required= True)

class IndimediPatient(models.Model):
    _inherit = 'hms.patient'

    @api.multi    
    def action_opp(self):
        return {
            'name': _('OPP'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'medical.procedure',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

class IndimediAppointment(models.Model):
    _inherit = 'hms.appointment'

    @api.multi
    def button_medical_procedure(self):
        return {
            'name': _('OPP'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'medical.procedure',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.patient_id.id)],
            'context': {'default_patient_id': self.patient_id.id,'default_app_id': self.id,'default_doctor_id':self.physician_id.id},
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: