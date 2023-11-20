# -*- coding: utf-8 -*-

from openerp import api, fields, models
import datetime

class ClaimReport(models.TransientModel):
    _name = 'claim.report'

    date_from = fields.Date(string='Start Date', default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)
    is_claim = fields.Boolean("Check For Created Date", default=True)

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'hms_insurance.claim_report')

    @api.multi
    def get_claim(self):
        claim_obj = self.env['hms.insurance.claim']
        if self.is_claim:
            domain = [('created_date', '>=', self.date_from),
                      ('created_date', '<=', self.date_to)]
        else:
            domain = [('date_received', '>=', self.date_from),
                      ('date_received', '<=', self.date_to)]
        claim_lines = claim_obj.search(domain)
        return claim_lines