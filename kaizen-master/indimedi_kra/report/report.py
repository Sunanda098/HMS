# # -*- coding: utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as
# #    published by the Free Software Foundation, either version 3 of the
# #    License, or (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
#  #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################

# import time
# from datetime import datetime
# from openerp.osv import osv
# from openerp.report import report_sxw



# class consultation_report(report_sxw.rml_parse):
#     def __init__(self, cr, uid, name, context=None):
#         super(consultation_report, self).__init__(cr, uid, name, context=context)
#         self.localcontext.update({
#             'time': time,
#             'get_appointment': self._get_appointment,
#             'get_pathology': self._get_pathology,
#             'get_radiology': self._get_radiology,
#             'get_prescription': self._get_prescription,
#         })

    # def _get_appointment(self):
    #     appontment_obj = self.pool.get('oemedical.appointment').browse(self.cr, self.uid,  self.ids)
    #     res = []
    #     appopintment_date=datetime.strptime(appontment_obj.appointment_day, '%Y-%m-%d %H:%M:%S')
    #     disc = {
    #         'appointment_id': appontment_obj.name,
    #         'patient_name': appontment_obj.patient_id.name,
    #         'appointment_day': appopintment_date.strftime("%d-%m-%Y"),
    #         'department': appontment_obj.building.name,
    #         'doctor': appontment_obj.doctor.name,
    #         'chief_complain': appontment_obj.chief_complain,
    #         'history_of_patient': appontment_obj.history_of_present_illness,
    #         'differencial_diagnosis': appontment_obj.differencial_diagnosis,
    #         'medical_advice': appontment_obj.medical_advice,
    #     }
    #     res.append(disc)
    #     return res

    # def _get_radiology(self):
    #     res = []
    #     disc ={}
    #     count = 1
    #     lab_obj = self.pool.get('oemedical.patient.lab.test').search(self.cr, self.uid, [('appointment', '=', self.ids)])
    #     lab_line = self.pool.get('oemedical.patient.radiology.test.line').search(self.cr, self.uid, [('line_id', '=', lab_obj)], {})
    #     lab_data = self.pool.get('oemedical.patient.radiology.test.line').browse(self.cr, self.uid, lab_line, {})
    #     for line in lab_data:
    #         disc ={
    #             'id': count,
    #             'instruction': line.instruction,
    #             'test': line.radiology_lab_id.name
    #         }
    #         count = count+1
    #         res.append(disc)
    #     return res

    # def _get_pathology(self):
    #     res = []
    #     disc = {}
    #     count = 1
    #     lab_obj = self.pool.get('oemedical.patient.lab.test').search(self.cr, self.uid, [('appointment', '=', self.ids)])
    #     lab_line = self.pool.get('oemedical.patient.lab.test.line').search(self.cr, self.uid, [('line_id', '=', lab_obj)], {})
    #     lab_data = self.pool.get('oemedical.patient.lab.test.line').browse(self.cr, self.uid, lab_line, {})
    #     for line in lab_data:
    #         disc ={
    #             'id': count,
    #             'instruction': line.instruction,
    #             'test': line.oemedical_lab_id.name,
    #         }
    #         count = count+1
    #         res.append(disc)
    #     return res

    # def _get_prescription(self):
    #     prescription_id = self.pool.get('oemedical.prescription.order').search(self.cr, self.uid, [('appointment', '=', self.ids)])
    #     prescription_line = self.pool.get('oemedical.prescription.line').search(self.cr, self.uid, [('name', '=', prescription_id)])
    #     prescription_date = self.pool.get('oemedical.prescription.line').browse(self.cr, self.uid, prescription_line, {})
    #     res = []
    #     disc ={}
    #     count = 1
    #     for prescription in prescription_date:
    #         disc ={
    #             'no': count,
    #             'prescription': prescription.template.product_id.name,
    #             'dose': prescription.dose,
    #             'unit': prescription.dose_unit.name,
    #             'common_dosage': prescription.common_dosage.name,
    #             'quantity': prescription.quantity,
    #             'days': prescription.days,
    #         }
    #         count+=1
    #         res.append(disc)
    #     return res

# class report_all_consultation(osv.AbstractModel):
#     _name = 'report.all_consultation_report.all_consultation_report_qweb'
#     _inherit = 'report.abstract_report'
#     _template = 'all_consultation_report.all_consultation_report_qweb'
#     _wrapped_report_class = consultation_report

# # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


from openerp import api, models

class ConsultationReport(models.AbstractModel):
    _name = 'report.all_consultation_report.all_consultation_report_qweb'

    @api.multi
    def _get_radiology(self, ids):
        res = []
        disc ={}
        lab_obj = self.pool.get('oemedical.patient.lab.test').search(self.env.cr, self.env.uid, [('appointment', '=', ids)])
        lab_line = self.pool.get('oemedical.patient.radiology.test.line').search(self.env.cr, self.env.uid, [('line_id', '=', lab_obj)])
        lab_data = self.pool.get('oemedical.patient.radiology.test.line').browse(self.env.cr, self.env.uid, lab_line)

        for line in lab_data:
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
        lab_obj = self.pool.get('oemedical.patient.lab.test').search(self.env.cr, self.env.uid, [('appointment', '=', ids)])
        lab_line = self.pool.get('oemedical.patient.lab.test.line').search(self.env.cr, self.env.uid, [('line_id', '=', lab_obj)])
        lab_data = self.pool.get('oemedical.patient.lab.test.line').browse(self.env.cr, self.env.uid, lab_line)
        for line in lab_data:
            disc ={
                'instruction': line.instruction,
                'test': line.oemedical_lab_id.name,
            }
            res.append(disc)
        return res

    def _get_prescription(self, ids):
        res = []
        disc ={}
        prescription_id = self.pool.get('oemedical.prescription.order').search(self.env.cr, self.env.uid, [('appointment', '=', ids)])
        prescription_line = self.pool.get('oemedical.prescription.line').search(self.env.cr, self.env.uid, [('name', '=', prescription_id)])
        prescription_date = self.pool.get('oemedical.prescription.line').browse(self.env.cr, self.env.uid, prescription_line)
        
        for prescription in prescription_date:
            disc ={
                'prescription': prescription.template.product_id.name,
                'dose': prescription.dose,
                'unit': prescription.dose_unit.name,
                'common_dosage': prescription.common_dosage.name,
                'quantity': prescription.quantity,
                'days': prescription.days,
            }
            res.append(disc)
        return res

    def _get_opp(self, ids):
        res = [] 
        disc = {}
        opp_id =self.pool.get('medical.procedure').search(self.env.cr, self.env.uid, [('appointment','=',ids)])
        opp_procedure_type = self.pool.get('medical.procedure').browse(self.env.cr, self.env.uid, opp_id).procedure_type.name
        disc = {
            'procedure_type': opp_procedure_type,
                } 
        res.append(disc)
        return res



    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('all_consultation_report.all_consultation_report_qweb')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'get_pathology': self._get_pathology,
            'get_radiology': self._get_radiology,
            'get_prescription': self._get_prescription,
            'get_opp': self._get_opp,

        }
        return report_obj.render('all_consultation_report.all_consultation_report_qweb', docargs)
