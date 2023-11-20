# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import re


class AccuseDetails(models.Model):
    _name = 'accuse.details'
    _rec_name = 'accuse_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Plaintiff'

    accuse_id = fields.Char(string='Claimant / Plaintiff')
    image = fields.Binary(string='Image', attachment=True)
    accuse_name = fields.Char(string='Name',track_visibility='onchange', required=True)
    accuse_mobile = fields.Char(string='Mobile', track_visibility='onchange', required=True)
    accuse_email = fields.Char(string='Email ID', track_visibility='onchange', required=True)
    accuse_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    accuse_dob = fields.Date(string='Birthdate', track_visibility='onchange')
    accuse_age = fields.Char(string='Age', track_visibility='onchange')
    accuse_marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
        'widowed', 'Widowed'), ('divorced', 'Divorced')], default="unmarried", string='Maritial Status', track_visibility='onchange')
    accuse_website = fields.Char(string='Website', track_visibility='onchange')
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(string='Street2..', track_visibility='onchange')
    city_id = fields.Char(string='City', track_visibility='onchange')
    state_id = fields.Many2one('res.country.state',string='State', ondelete='restrict', track_visibility='onchange')
    zip = fields.Char(track_visibility='onchange')
    district_id = fields.Char(string='District', track_visibility='onchange')
    country_id = fields.Many2one('res.country',string='Country', ondelete='restrict', track_visibility='onchange')
    account = fields.Integer(
        compute="_compute_account_count", string='Account')
    village = fields.Char(string='Village', track_visibility='onchange')
    account_details_ids = fields.One2many(
        'account.master', 'accuse_account', string='Account')
    accuse_document_ids = fields.One2many(
        'accuse.document', 'accuse_document_id',string='Documents')
    postal_street = fields.Char(string='Postal Street',track_visibility='onchange')
    postal_street2 = fields.Char(string='Postal Street2..',track_visibility='onchange')
    postal_city_id = fields.Char(string='Postal City',track_visibility='onchange')
    postal_village = fields.Char(string='Village',track_visibility='onchange')
    postal_state_id = fields.Many2one(
        'res.country.state', string='Postal State', ondelete='restrict',track_visibility='onchange')
    postal_zip = fields.Char(string='Postal zip')
    district_id = fields.Char(string='District', track_visibility='onchange')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict',track_visibility='onchange')
    a_doc_count = fields.Integer(
        compute="_compute_adoc_count", string='Document',track_visibility='onchange')
    accuse_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    all_case_ids = fields.One2many(
        'matter.matter', 'accused', string='Cases')#, domain=lambda self: [('case_result','=','on_going')])
    # won_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases won', domain=lambda self: [('case_result','=','won')])
    # lost_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases lost', domain=lambda self: [('case_result','=','lost')])
    # settlement_case_ids = fields.One2many(
    #     'matter.matter', 'accused', string='Cases settled', domain=lambda self: [('case_result','=','settlement')])


    _sql_constraints = [('name_uniq', 'UNIQUE(accuse_mobile,accuse_email)', 'Mobile No. & Email-ID Must Be Unique!')]
    
    @api.model
    def create(self, values):
        if values.get('accuse_mobile', ''):
            mobile = values.get('accuse_mobile', '')
            if mobile.isdigit():
                pass
            else:
                raise ValidationError(
                    _('Enter Only Numerical Value in Mobile No.'))
        return super(AccuseDetails, self).create(values)
    
    @api.onchange('accuse_dob')
    def onchange_accuse_dob(self):
        if self.accuse_dob:
            b_date = datetime.strptime(self.accuse_dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.accuse_age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))

    @api.onchange('accuse_email')
    def validate_mail(self):
       if self.accuse_email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.accuse_email)
        if match == None:
            raise ValidationError('Not a valid E-mail ID')

    #Button
    @api.multi
    def action_accuse_account_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('accuse_account', '=', self.id)]
            action['context'] = ({'default_account_holder': 'accuse',
                                  'default_accuse_account': self.id or False})
            return action

    @api.multi
    def action_accuse_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.accuse_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('accuse_document_id', 'in', [self.id])]
            action['context'] = ({'default_accuse_document_id': self.id})
            return action

    #Count
    @api.multi
    def _compute_account_count(self):
        accountLine = self.env['account.master']
        for partner in self:
            partner.account = accountLine.search_count(
                [('accuse_account', '=', partner.id)])

    @api.multi
    def _compute_adoc_count(self):
        DocLine = self.env['accuse.document']
        for doc in self:
            doc.a_doc_count = DocLine.search_count(
                [('accuse_document_id', '=', doc.id)])

class AccuseName(models.Model):
    _name = 'accuse.name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name',required=True,track_visibility='onchange')

class AccuseIDocument(models.Model):
    _name = 'accuse.document'
    _rec_name = 'accuse_document_id'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    
    doc_name = fields.Selection(
        [('national_id', 'National ID'), ('passport', 'Passport'), ('dl', 'Driver’s License'), ('other','Other')], default="national_id", string='Document Type', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment',string='Attachments',track_visibility='onchange')
    comment = fields.Text(string='Description',track_visibility='onchange')
    date = fields.Date(string='Date',default=fields.Date.today())
    ad_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    accuse_document_id = fields.Many2one('accuse.details',string='Claimant / Plaintiff Document')