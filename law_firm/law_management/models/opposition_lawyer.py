# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import re


class OppositionLawyer(models.Model):
    _name = 'opposition.lawyer'
    _rec_name = 'opposition_lawyer_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']

    opposition_id = fields.Char(string='Opposition ID')
    opposition_lawyer_name = fields.Char(string='Name', ondelete="cascade", track_visibility='onchange', required=True)
    image = fields.Binary(string='Image', attachment=True)
    opposition_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    opposition_dob = fields.Date(
        string='Birthdate', track_visibility='onchange')
    opposition_age = fields.Char(string='Age', track_visibility='onchange')
    oppposition_marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
        'widowed', 'Widowed'), ('divorced', 'Divorced')], default="unmarried", string='Maritial Status', track_visibility='onchange')
    opposition_mobileP = fields.Char(
        string='Mobile(Personal)', track_visibility='onchange')
    opposition_mobileW = fields.Char(
        string='Mobile(Work)', track_visibility='onchange', required=True)
    opposition_emailP = fields.Char(
        string='Email(Personal)', track_visibility='onchange')
    opposition_emailW = fields.Char(
        string='Email(Work)', track_visibility='onchange', required=True)
    opposition_website = fields.Char(
        string='Website', track_visibility='onchange')
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(string='Street2..', track_visibility='onchange')
    city_id = fields.Char(string='City', track_visibility='onchange')
    state_id = fields.Many2one(
        'res.country.state', string='State', ondelete='restrict', track_visibility='onchange')
    zip = fields.Char(string='zip',
                      track_visibility='onchange')
    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict', track_visibility='onchange')
    village = fields.Char(string='Village', track_visibility='onchange')
    account = fields.Integer(
        compute="_compute_account_count", string='Account')
    district_id = fields.Char(string='District', track_visibility='onchange')
    oppposition_nationality = fields.Char(string='Nationality')
    account_details_ids = fields.One2many(
        'account.master', 'opp_lawyer_account', string='Account')
    opp_lawyer_doc_ids = fields.One2many(
        'opp.lawyer.document', 'opp_lawyer_document_id', string='Documents')
    postal_street = fields.Char(string='Postal Street')
    postal_street2 = fields.Char(string='Postal Street2..')
    postal_city_id = fields.Char(string='Postal City')
    postal_village = fields.Char(string='Village')
    postal_state_id = fields.Many2one(
        'res.country.state', string='Postal State', ondelete='restrict')
    postal_zip = fields.Char(string='Postal zip')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    district_id = fields.Char(string='District', track_visibility='onchange')
    ol_doc_count = fields.Integer(
        compute="_compute_ldoc_count", string='Document')
    opp_lawyer_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")

    @api.onchange('opposition_dob')
    def onchange_lawyer_dob(self):
        if self.opposition_dob:
            b_date = datetime.strptime(self.opposition_dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.opposition_age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))

    @api.onchange('opposition_emailP', 'opposition_emailW')
    def validate_mail(self):
        if self.opposition_emailP:
            match = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.opposition_emailP)
            if match == None:
                raise ValidationError('Personal E-mail ID is Not Valid!!!')
        if self.opposition_emailW:
            match = re.match(
                '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.opposition_emailW)
            if match == None:
                raise ValidationError('Work E-mail ID is Not Valid!!!')

    # Button
    @api.multi
    def action_opposition_lawyer_account_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('opp_lawyer_account', '=', self.id)]
            action['context'] = ({'default_account_holder': 'opp_lawyer',
                                  'default_opp_lawyer_account': self.id or False})
            return action

    @api.multi
    def action_opp_lawyer_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.opp_lawyer_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('opp_lawyer_document_id', 'in', [self.id])]
            action['context'] = ({'default_opp_lawyer_document_id': self.id})
            return action

    # Count
    @api.multi
    def _compute_account_count(self):
        accountLine = self.env['account.master']
        for partner in self:
            partner.account = accountLine.search_count(
                [('opp_lawyer_account', '=', partner.id)])

    @api.multi
    def _compute_ldoc_count(self):
        DocLine = self.env['opp.lawyer.document']
        for doc in self:
            doc.ol_doc_count = DocLine.search_count(
                [('opp_lawyer_document_id', '=', doc.id)])


class OppLawyerDocument(models.Model):
    _name = 'opp.lawyer.document'
    _order = 'create_date desc'
    _rec_name = 'opp_lawyer_document_id'
    _inherit = ['mail.thread']

    doc_name = fields.Selection(
        [('national_id', 'National ID'), ('passport', 'Passport'), ('dl', 'Driver’s License'), ('other','Other')], default="national_id", string='Document Type', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment', string='Attachments')
    comment = fields.Text(string='Description')
    date = fields.Date(string='Date')
    ol_d_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    opp_lawyer_document_id = fields.Many2one(
        'opposition.lawyer', string='Opposition Lawyer')