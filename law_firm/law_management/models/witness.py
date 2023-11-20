# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re

class WitnessDetails(models.Model):
    _name = 'witness.details'
    _rec_name = 'witness_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Witness'

    witness_id = fields.Char(string='Witness ID')
    image = fields.Binary(string='Image',attachment=True, track_visibility='onchange')
    witness_name = fields.Char(string='Witness',track_visibility='onchange', required=True)
    witness_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default="male", string='Gender', track_visibility='onchange')
    witness_dob = fields.Date(string='Birthdate', track_visibility='onchange')
    witness_age = fields.Char(string='Age', track_visibility='onchange')
    witness_marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('single', 'Single'), (
        'widowed', 'Widowed'), ('divorced', 'Divorced')], default="unmarried", string='Maritial Status', track_visibility='onchange')
    witness_mobile = fields.Char(string='Mobile', track_visibility='onchange', required=True)
    witness_email = fields.Char(string='Email', track_visibility='onchange', required=True)
    witness_website = fields.Char(string='Website', track_visibility='onchange')
    witness_past_criminal = fields.Boolean(
        string='IS Past Criminal Record?', track_visibility='onchange')
    district_id = fields.Char(string='District', track_visibility='onchange')
    witness_past_criminal_details = fields.Text(
        'Past Criminal Record Note', track_visibility='onchange')
    village = fields.Char(string='Village', track_visibility='onchange')
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(string='Street2..', track_visibility='onchange')
    city_id = fields.Char(string='City', track_visibility='onchange')
    state_id = fields.Many2one('res.country.state',string='State', ondelete='restrict', track_visibility='onchange')
    zip = fields.Char(string='zip',
                      track_visibility='onchange')
    country_id = fields.Many2one('res.country',string='Country', ondelete='restrict', track_visibility='onchange')
    witness_nationality = fields.Char(string='Nationality', track_visibility='onchange')
    witness_doc_ids = fields.One2many(
        'witness.document', 'witness_document_id', string='Documents')
    postal_street = fields.Char(string='Postal Street', track_visibility='onchange')
    postal_street2 = fields.Char(string='Postal Street2..', track_visibility='onchange')
    postal_city_id = fields.Char(string='Postal City', track_visibility='onchange')
    postal_village = fields.Char(string='Village', track_visibility='onchange')
    postal_state_id = fields.Many2one(
        'res.country.state', string='Postal State', ondelete='restrict', track_visibility='onchange')
    district_id = fields.Char(string='District', track_visibility='onchange')
    postal_zip = fields.Char(string='Postal zip', track_visibility='onchange')
    postal_country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict', track_visibility='onchange')
    w_doc_count = fields.Integer(
        compute="_compute_wdoc_count")
    witness_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")


    @api.model
    def create(self, values):
        values['witness_id'] = self.env[
            'ir.sequence'].next_by_code('witness.details') or ''
        if values.get('witness_mobile', ''):
            mobile = values.get('witness_mobile', '')
            if mobile.isdigit():
                pass
            else:
                raise ValidationError(
                    _('Enter Only Numerical Value in Mobile No.'))
        return super(WitnessDetails, self).create(values)

    @api.onchange('witness_dob')
    def onchange_witness_dob(self):
        if self.witness_dob:
            b_date = datetime.strptime(self.witness_dob, '%Y-%m-%d')
            delta = relativedelta(datetime.now(), b_date)
            if delta.years <= 2:
                age = _("%syear %smonth %sday") % (
                    delta.years, delta.months, delta.days)
            else:
                age = _("%s Year") % (delta.years)
            self.witness_age = age
            if delta.days < 0:
                raise UserError(('You cannot enter Future DATE OF BIRTH'))

    @api.onchange('witness_email')
    def validate_mail(self):
       if self.witness_email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.witness_email)
        if match == None:
            raise ValidationError('Not a valid E-mail ID')

    @api.multi
    def action_witness_document(self):
        self.ensure_one()
        action_rec = self.env.ref(
            'law_management.witness_document_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('witness_document_id', 'in', [self.id])]
            action['context'] = ({'default_witness_document_id': self.id})
            return action

    #Count
    @api.multi
    def _compute_wdoc_count(self):
        DocLine = self.env['witness.document']
        for doc in self:
            doc.w_doc_count = DocLine.search_count(
                [('witness_document_id', '=', doc.id)])


class WitnessDocument(models.Model):
    _name = 'witness.document'
    _rec_name = 'witness_document_id'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    
    doc_name = fields.Selection(
        [('national_id', 'National ID'), ('passport', 'Passport'), ('dl', 'Driver’s License'), ('other','Other')], default="national_id", string='Document Type', track_visibility='onchange')
    doc_no = fields.Char(string='Document No.')
    doc_id = fields.Many2many('ir.attachment',string='Attachments')
    comment = fields.Text(string='Description', track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    wd_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    witness_document_id = fields.Many2one('witness.details',string='Witness')