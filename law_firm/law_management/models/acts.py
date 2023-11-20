# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
import time

class ActAct(models.Model):
    _name = 'act.act'
    _rec_name = 'act_no'
    _order = 'create_date desc'
    _inherit = ['mail.thread']
    _description = 'Act'

    act_seq  = fields.Char(
        size=256, string='ACT Seq', readonly=True, default='New ACT', copy=False)
    act_no = fields.Char(string='Act No',track_visibility='onchange')
    act_name = fields.Many2one('act.act.name',string='Act Name',track_visibility='onchange')
    act_type = fields.Selection(
        [('criminal', 'Criminal'), ('civil', 'Civil')], string='Act Type',track_visibility='onchange')
    act_link = fields.Char(string='Link',track_visibility='onchange')
    act_year = fields.Char(string='Act Year',track_visibility='onchange')
    act_desc = fields.Html(string='Act Description',track_visibility='onchange')

class ActActName(models.Model):
    _name = 'act.act.name'
    _order = 'create_date desc'
    

    name = fields.Char(string='Name',required=True)