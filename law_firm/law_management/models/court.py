# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time
import re


class CourtCourt(models.Model):
    _name = 'court.court'
    _rec_name = 'court_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Court'

    court_admin = fields.Many2one('court.admin', string="Court Admin")
    case_clerk = fields.Many2one('case.clerk', string="Registry Clerk")
    court_name = fields.Char(string='Court Name',track_visibility='onchange')
    court_email = fields.Char(string='Email', required=True,track_visibility='onchange')
    fax_no = fields.Char(string='Fax No.')
    count_number = fields.Char(string='Contact No.', required=True,track_visibility='onchange')
    court_number1 = fields.Char(string="Phone")
    court_judge = fields.Many2one('judge.details',string='Judge Name',track_visibility='onchange')
    judge_details_ids = fields.One2many(
        'judge.details', 'judge_details_id', string='Judge Details')
    street = fields.Char(string='Street', track_visibility='onchange')
    street2 = fields.Char(string='Street2..', track_visibility='onchange')
    city_id = fields.Char(string='City', track_visibility='onchange')
    state_id = fields.Many2one(
        "res.country.state", string='State', ondelete='restrict', track_visibility='onchange')
    zip = fields.Char(string='zip', track_visibility='onchange')
    district_id = fields.Char(string='District', track_visibility='onchange')
    country_id = fields.Many2one('res.country',
                                 string='Country', ondelete='restrict', track_visibility='onchange')
    room_status_court = fields.Selection(
        [('available', 'Available'), ('not_available', 'Not Available')],string='Court Availability',track_visibility='onchange')
    account = fields.Integer(
        compute="_compute_account_count", string='Account')
    count_court_judge = fields.Integer(string='Judge',compute='_compute_judge_count')
    account_details_ids = fields.One2many(
        'account.master', 'court_id', string='Account')
    court_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    court_category = fields.Many2one('court.category', string="Court Category")

    @api.model
    def create(self, values):
        if values.get('count_number', ''):
            mobile = values.get('count_number', '')
            if mobile.isdigit():
                pass
            else:
                raise ValidationError(
                    _('Enter Only Numerical Value in Mobile No.'))
        return super(CourtCourt, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('count_number', ''):
            mobile = values.get('count_number', '')
            if mobile.isdigit():
                pass
            else:
                raise ValidationError(
                    _('Enter Only Numerical Value in Mobile No.'))
        return super(CourtCourt, self).write(values)

    @api.multi
    def _compute_account_count(self):
        accountLine = self.env['account.master']
        for court in self:
            court.account = accountLine.search_count(
                [('court_id', '=', court.id)])

    # @api.multi
    # def _compute_account_count(self):
    #     for count in self:
    #         count.account = len(count.account_details_ids)

    @api.multi
    def _compute_judge_count(self):
        JudgeLine = self.env['judge.details']
        for judge in self:
            judge.count_court_judge = JudgeLine.search_count(
                [('judge_details_id', '=', judge.id)])


    @api.multi
    def action_court_account_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.account_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('court_id', '=', self.id)]
            action['context'] = ({'default_account_holder': 'court',
                                  'default_court_id': self.id or False})
            return action

    @api.multi
    def action_court_judge_view(self):
        self.ensure_one()
        action_rec = self.env.ref('law_management.judge_details_action')
        if action_rec:
            action = action_rec.read()[0]
            result = []
            action['domain'] = [('judge_details_id', '=', self.id)]
            action['context'] = ({'default_judge_details_id':self.id,
                                })
            return action

    @api.onchange('court_email')
    def validate_mail(self):
       if self.court_email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.court_email)
        if match == None:
            raise ValidationError('Not a valid E-mail ID')

class CourtRoom(models.Model):
    _name = 'court.room'
    _rec_name = 'name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    
    name = fields.Char(string="Room No.",track_visibility='onchange')
    court_id = fields.Many2one('court.court', string="Court",track_visibility='onchange')
    room_status = fields.Selection(
        [('available', 'Available'), ('not_available', 'Not Available')],string='Room Status',track_visibility='onchange')
    court_room_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")


class CourtFees(models.Model):
    _name = 'court.fees'
    _order = 'create_date desc'
    _rec_name = 'court_name'
    _inherit = ['mail.thread']

    matter_id = fields.Many2one('matter.matter', string="Case Number",track_visibility='onchange',required=True)
    fees_case_name = fields.Char(related='matter_id.case_name', string='Case Name')
    client_name = fields.Many2one('client.client',related='matter_id.client_name',string='Client Name',track_visibility='onchange',required=True)
    accuse_name = fields.Many2one('accuse.details',related='matter_id.accused',string='Claimant / Plaintiff Name',track_visibility='onchange')
    client_ids = fields.Many2many(related='matter_id.client_name_many')
    accuse_ids = fields.Many2many(related='matter_id.accuse_ids')
    court_name = fields.Many2one('court.court',related='matter_id.court_id',string='Court Name',track_visibility='onchange',required=True)
    amount = fields.Float(string='Amount',track_visibility='onchange')
    date = fields.Date('Date',default=fields.Date.today(),track_visibility='onchange')
    payment_date = fields.Date(string='Date of Payment',track_visibility='onchange')
    rec_no = fields.Char(string='Receipt No.',track_visibility='onchange')
    is_paid = fields.Boolean(string='Is Paid',track_visibility='onchange')
    court_fees_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user, readonly="True")
    description = fields.Html(string='Description')
    

class CourtName(models.Model):
    _name = 'court.name'

    name = fields.Char(string='Name',required=True)

class CourtCategory(models.Model):
    _name = 'court.category'

    name = fields.Char(string="name", required=True)