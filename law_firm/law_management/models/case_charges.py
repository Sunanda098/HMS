# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time


class CaseCharges(models.Model):
    _name = 'case.charge'
    _rec_name = 'case_name'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Case Charge'


    case_name = fields.Many2one("matter.matter", string="Case Number",
        track_visibility='onchange')
    charges_case_name = fields.Char(related='case_name.case_name', string='Case Name')
    client_name = fields.Many2one('client.client',string='Client', track_visibility='onchange')
    accuse_name = fields.Many2one('accuse.details',string="Accuse")
    number = fields.Many2one("law.code", string="Law Code",
        track_visibility='onchange')
    date = fields.Date(string="Date",default=fields.Date.today(),
        track_visibility='onchange')
    amount = fields.Float(sting='Amount',track_visibility='onchange')
    desciption = fields.Html("Description",track_visibility='onchange')
    case_charges_created_by = fields.Many2one(
        'res.users', string="Created By", default=lambda self: self.env.user,
        readonly="True")
    client_ids = fields.Many2many(related='case_name.client_name_many')
    accuse_ids = fields.Many2many(related='case_name.accuse_ids')
    laws_desc = fields.Char(related="number.short_des")