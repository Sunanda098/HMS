# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class Appointment(models.Model):
    _inherit = 'hms.appointment'
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('waiting', 'Waiting'),
        ('next', 'Next'),
        ('in_consultation', 'In consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('invoiced', 'Invoiced'),
        ('invoice_exempt', 'Invoice Exempt'),
    ], string='State',default='draft')
    
    
    @api.one
    def appointment_next(self):
        self.state = 'next'
