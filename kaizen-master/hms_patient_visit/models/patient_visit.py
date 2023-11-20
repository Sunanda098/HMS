# -*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models , _
from openerp.exceptions import UserError

class PatientVisit(models.Model):
    _name = 'indi.patient.visit'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Indimedi Patient Visits'
    
    
    name = fields.Char(string="Patient Visit #", required=True, readonly=True,default='New')
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirmed'),('done', 'Done')], string='State',default='draft')
    patient_id = fields.Many2one('hms.patient', string="Patient", required='True')
    visitor_name = fields.Char(string="Visitor's Name", required='True')
    date = fields.Datetime(string='Visit Date', readonly="True",default=fields.Datetime.now)
    contact_no = fields.Char(string="Visitor's Contact No.",required='True')
    note = fields.Text(string="Notes")
    
    
    @api.multi
    def confirm_visit(self):
        self.name = self.env['ir.sequence'].next_by_code('indi.patient.visit')
        self.state = 'confirm'

    @api.multi
    def done_visit(self):
        self.state = 'done'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: