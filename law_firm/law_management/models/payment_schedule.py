# coding: utf-8

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class PaymentSchedule(models.Model):
    _name = "payment.schedule"
    _rec_name = 'name'
    _order = 'case_id asc'
    _inherit = ['mail.thread']

    name = fields.Char(string="Payment Milestone ID")
    schedule_date = fields.Date(string="Schedule Date of Payment")
    description = fields.Text(string="Description")
    paid_amount = fields.Float(string="Amount")
    paid_by = fields.Selection([
                            ('accused', 'Claimant / Plaintiff'),
                            ('court', 'Court')], string="Paid By")
    claim_distribution_id = fields.Many2one("claim.distribution", string="Claim Distribution ID")
    is_paid = fields.Boolean(string="Is Paid")
    case_id = fields.Many2one("matter.matter", related='claim_distribution_id.case_id', string="Case Number")
    court_id = fields.Many2one('court.court', related='claim_distribution_id.court_id', string="Court")
    payment_case_name = fields.Char(related='case_id.case_name', string='Case Name')

    @api.model
    def create(self,vals):
        res = super(PaymentSchedule,self).create(vals)
        sequence_code = self.env['ir.sequence'].next_by_code('payment.schedule')
        res.update({'name':sequence_code})
        return res
