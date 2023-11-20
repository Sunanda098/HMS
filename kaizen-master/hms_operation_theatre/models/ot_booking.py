# -*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import datetime, date, timedelta

class product_template(models.Model):
    _inherit = "product.template"

    hospital_product_type = fields.Selection(selection_add=[('package','Package')])
    package_note = fields.Text("Package Description")

class ImplantCompany(models.Model):
    _name = 'implant.company'

    name = fields.Char('Company Name')

class HmsImplant(models.Model):
    _name = 'hms.implant'

    name = fields.Char('Implant')


class OtBooking(models.Model):
    _name = 'ot.booking'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.multi
    def button_confirm(self):
        self.state = 'confirm'
        self.name = self.env['ir.sequence'].next_by_code('ot.booking') or ''

    @api.multi
    def button_cancel(self):
        self.state = 'cancel'
   
    @api.multi
    def button_done(self):
        self.state = 'done'

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.note = self.product_id.package_note

    @api.model
    def _get_package_id(self):
        return self.product_id.search([('hospital_product_type', '=', "package")], limit=1).id

    @api.model
    def _get_end_date(self):
        return datetime.now() + timedelta(hours=2)
    
    @api.multi
    @api.depends('end_date')
    def _get_end_time(self):
        for rec in self:
            rec.end_time = '-' + str(datetime.time(datetime.strptime(rec.end_date, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5,minutes=30))).rpartition(':')[0] + 'p'

    name = fields.Char(string="OT #", required=True, readonly=True,default='New')
    patient_id = fields.Many2one('hms.patient', 'Patient', required="True")
    image = fields.Binary(related='patient_id.image',string='Image') 
    start_date = fields.Datetime('Start Date', default=fields.Datetime.now)
    end_date = fields.Datetime('End Date', default=_get_end_date)
    operation_id = fields.Many2one('hms_surgery', 'Operation')
    side = fields.Selection([('none', 'None'), ('right', 'Right'), ('left', 'Left'), ('both', 'Both')], default="none")
    implant = fields.Many2one('hms.implant', 'Implant')
    implant_company = fields.Many2one('implant.company', 'Implant Company')
    cashles = fields.Selection([('yes','Yes'),('no','No')], 'Cashless')
    product_id = fields.Many2one('product.product', string='Package', help="Package", domain=[('hospital_product_type', '=', "package")], required=True, default=_get_package_id)
    note = fields.Text('Note')
    ward = fields.Many2one('hospital.ward',string='Ward/Room')
    bed = fields.Many2one ('hospital.bed',string='Bed No.')
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirmed'),('cancel', 'Cancelled'),('done', 'Done'),], string='Status', default='draft')
    ot_id = fields.Many2one('indimedi.hospital.or','OT')
    end_time = fields.Char('End time',compute="_get_end_time")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: