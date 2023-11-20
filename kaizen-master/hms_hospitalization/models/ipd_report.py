# -*- coding: utf-8 -*-

from openerp import api, fields, models
import datetime

class IpdReport(models.TransientModel):
    _name = 'ipd.report'

    date_from = fields.Date(string='Start Date', default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)
    is_discharge = fields.Boolean("Select to choose Discharge basis", default=False)

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'hms_hospitalization.ipd_report')

    @api.multi
    def get_hospitalization(self):
        hospitalization_obj = self.env['inpatient.registration']
        if self.is_discharge:
            domain = [('discharge_date', '>=', self.date_from),
                      ('discharge_date', '<=', self.date_to)]
        else:
            domain = [('hospitalization_date', '>=', self.date_from),
                      ('hospitalization_date', '<=', self.date_to)]
        hospital_lines = hospitalization_obj.search(domain)
        return hospital_lines