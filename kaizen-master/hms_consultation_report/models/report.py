# # -*- coding: utf-8 -*-

from openerp import api, models

class ConsultationReport(models.AbstractModel):
    _name = 'report.hms_consultation_report.consultation_report_qweb'

    @api.multi
    def _get_radiology(self, ids):
        res = []
        disc ={}
        lab_line = self.env['hms.patient.laboratory.test.line'].search([('line_id.appointment', '=', ids)])
        for line in lab_line:
            disc ={
                'instruction': line.instruction,
                'test': line.radiology_lab_id.name
            }
            res.append(disc)
        return res


    @api.multi
    def _get_pathology(self, ids):
        res = []
        disc = {}
        lab_line = self.env['hms.patient.laboratory.test.line'].search([('line_id.appointment', '=', ids)])
        for line in lab_line:
            disc ={
                'instruction': line.instruction,
                'test': line.hms_lab_id.name,
            }
            res.append(disc)
        return res

    @api.multi
    def _get_past_surgeries(self, ids):
        res = []
        disc ={}
        print "##IDs",ids
        past_surgeries_line = self.env['past.surgeries'].search([('appointment_id', '=', ids)])
        for ps_rec in past_surgeries_line:
            disc ={
                'result': ps_rec.result,
                'date': ps_rec.date,
                'hosp_or_doctor': ps_rec.hosp_or_doctor,
                'description': ps_rec.description,
            }
            res.append(disc)
        return res

    @api.multi
    def _get_prescription(self, ids):
        res = []
        disc ={}
        print "##IDs",ids
        prescription_line = self.env['prescription.line'].search([('appointment_id', '=', ids)])
        for prescription in prescription_line:
            disc ={
                'prescription': prescription.product_id.name,
                'dose': prescription.dose,
                'unit': prescription.dose_unit.name,
                'common_dosage': prescription.common_dosage.name,
                'sub_frequency_id': prescription.sub_frequency_id.name,
                'quantity': prescription.quantity,
                'days': prescription.days,
            }
            res.append(disc)
        return res

    def _get_opp(self, ids):
        res = [] 
        disc = {}
        opp_id =self.env['medical.procedure'].search([('app_id','=', ids)], limit=1)
        disc = {
            'procedure_type': opp_id.procedure_type.name,
                } 
        res.append(disc)
        return res

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hms_consultation_report.consultation_report_qweb')
        docargs = {
                'doc_ids': self._ids,
                'doc_model': report.model,
                'docs': self.env[report.model].browse(self._ids),
                'get_pathology': self._get_pathology,
                'get_radiology': self._get_radiology,
                'get_prescription': self._get_prescription,
                'get_opp': self._get_opp,
        }
        return report_obj.render('hms_consultation_report.consultation_report_qweb', docargs)
