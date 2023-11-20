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


from openerp import api, models

class ConsultationInvoiceReport(models.AbstractModel):
    _name = 'report.hms_consultation_report.invoice_qweb_report'

    def _get_investigation_invoice(self, total_balance=None):
        amount_total = 0
        res = []
        appointment = self.env['hms.appointment']
        if appointment.invoice_id.id:
            amount_total += appointment.invoice_id.amount_total
            res.append(appointment.invoice_id.id)
        invoice_obj = self.env['account.invoice']
        #what is 2 still not clear
        if appointment.product_id.id == 2 and appointment.patient_id.invoice_id.id:
            res.append(appointment.patient_id.invoice_id.id)
            amount_total += appointment.patient_id.invoice_id.amount_total

        labtest_obj = self.env['hms.patient.lab.test']
        labtest_ids = labtest_obj.search([('appointment','=',self.ids)])
        for lab in labtest_ids:
            if lab.invoice_id.id:
                res.append(lab.invoice_id.id)
                amount_total += lab.invoice_id.amount_total

        invoice_line_obj = self.env['account.invoice.line']
        invoice_line_ids = invoice_line_obj.search([('invoice_id', 'in', res)])
        invoice_lines = invoice_line_obj.browse(invoice_line_ids)
        amount_in_word = self.env['account.voucher'].amount_to_text(amount_total)
        if total_balance:
            self.amount_total = amount_total
            self.amount_in_word = amount_in_word
        else:
            return invoice_lines
        
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hms_consultation_report.invoice_qweb_report')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'get_investigation_invoice': self._get_investigation_invoice
        }
        return report_obj.render('hms_consultation_report.invoice_qweb_report', docargs)
