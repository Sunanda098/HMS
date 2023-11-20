# -*- coding: utf-8 -*-

import time
from openerp import api, models
import time
from datetime import datetime, timedelta
import pytz

class TreatmentSheet(models.AbstractModel):
    _name = 'report.hms_treatment.report_treatmentsheet'

    def _get_medicines(self):
        res = []
        inpatients = self.env['inpatient.registration'].search([('id','=',self.ids[0])])
        treatment = self.env['hms.treatment']
        medicines = []
        if inpatients and inpatients.treatment_ids:
            latest_treatment_id = max(inpatients.treatment_ids.ids)
            treatment = self.env['hms.treatment'].browse(latest_treatment_id)
            cur_product_ids = []
            all_products_ids = []
            new_product_ids = []
            for current_medicine in treatment.prescription_line:
                cur_product_ids.append(current_medicine.product_id.id)
            for record in inpatients.treatment_ids:
                for line in record.prescription_line:
                    if record.id != treatment.id:
                        all_products_ids.append(line.product_id.id)
            for cur_id in cur_product_ids:
                if cur_id not in all_products_ids:
                    new_product_ids.append(cur_id)
            medicines = self.env['prescription.line'].search([('product_id','in',new_product_ids),('treatment_id','=',treatment.id)])
        return medicines

    def _get_treatments(self):
        res = []
        inpatients = self.env['inpatient.registration'].search([('id','=',self.ids[0])])
        treatment = self.env['hms.treatment']
        if inpatients and inpatients.treatment_ids:
            latest_treatment_id = max(inpatients.treatment_ids.ids)
            treatment = self.env['hms.treatment'].browse(latest_treatment_id)
        return treatment
    
    @api.multi
    def render_html(self, data):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hms_treatment.report_treatmentsheet')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'treatments': self._get_treatments(),
            'medicines':self._get_medicines()
        }
        return self.env['report'].render('hms_treatment.report_treatmentsheet', docargs)
