# -*- coding: utf-8 -*-
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import UserError, ValidationError
from datetime import datetime

class IndiLithoStone(models.Model):
    _name = 'litho.stone'

    name = fields.Char('Name')


class IndiLithoStoneLines(models.Model):
    _name = 'litho.stone.line'

    stone = fields.Many2one('litho.stone', string='Description')
    size = fields.Integer(string='Size')
    litho_id = fields.Many2one('hms.lithotripsy',string='Inpatient')
    mm_lable = fields.Char('MM', readonly=True, default='mm')


class Lithotripsy(models.Model):
    _name = 'hms.lithotripsy'
    _description = 'Indimedi Lithotripsy'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string='Lithotripsy', readonly=True, default="New")
    patient_id = fields.Many2one('hms.patient', string='Patient', reaquired=True, track_visibility='always')
    inpatient_id =fields.Many2one('inpatient.registration', string="Hospitalization")
    doctor_id = fields.Many2one('hms.physician', string='Doctor', reaquired=True)
    ref_doctor_id = fields.Many2one('hms.physician', string='Reffering Doctor')
    date_start = fields.Datetime(string='Start Date',default=fields.Datetime.now)
    date_end = fields.Datetime(string='End Date')
    product_id = fields.Many2one('product.product', string='Product')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    stone_line_ids = fields.One2many('litho.stone.line', 'litho_id', string='Stone')
    diagnosis = fields.Text(string='Diagnosis')
    procedure = fields.Text(string='Procedure')
    advice = fields.Text(string='Advice')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('progress', 'In Progress'), ('invoiced', 'Invoiced'), ('done', 'Done')], string='Status', default='draft', track_visibility='always')
    
    @api.multi
    @api.onchange('patient_id')
    def _onchange_patient(self):
        if self.patient_id:
            hosp_ids = self.inpatient_id.search([('patient_id', '=', self.patient_id.id), ('state', 'in', ['hosp', 'discharged', 'done'])])
            self.inpatient_id = hosp_ids and hosp_ids[-1] or False

    @api.multi
    def action_confirm(self):
        if self.name  == 'New':
            code = self.env['ir.sequence'].next_by_code('hms.lithotripsy') or 'New'
            self.write({'name': code, 'state': 'confirm'})
        return True

    @api.one
    def action_inprogress(self):
        self.state = 'progress'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.multi
    def action_create_invoice(self):
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']
        inv_line_obj = self.env['account.invoice.line']
        reg_product_obj = self.env['product.product']
        product_id = self.product_id
        account_id = False
        if product_id.id:
            account_id = product_id.product_id.property_account_income_id.id
        if not account_id:
            prop = self.env['ir.property'].get('property_account_income_categ_id', 'product.category')
            account_id = prop and prop.id or False
        invoice = inv_obj.create({
            'account_id': self.patient_id.partner_id.property_account_receivable_id.id,
            'partner_id': self.patient_id.partner_id.id,
            'type': 'out_invoice',
            'name': '-',
            'origin': self.name,
            'currency_id': self.env.user.company_id.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': product_id.name,
                'price_unit': product_id.lst_price,
                'account_id': account_id,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': product_id.uom_id.id,
                'product_id': product_id.id,
                'account_analytic_id': False,
            })],
        })
        return self.write({'state': 'invoiced', 'invoice_id': invoice.id})

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

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def unlink(self):
        """Allows to delete in draft state"""
        if self.state != 'draft':
            raise ValidationError(_('Lithotripsy can be delete only in Draft state.'))
        return super(Procedure, self).unlink()

class IndimediPatient (models.Model):
    _inherit = "hms.patient"

    @api.multi
    def action_lithotripsy(self):
        return {
            'name': _('OPP'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hms.lithotripsy',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: