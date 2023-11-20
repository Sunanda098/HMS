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
    _name = 'report.all_consultation_report.all_consultation_invoice_qweb_report'

    def _get_investigation_invoice(self, ids, total_balance=None):
        amount_total = 0
        res = []
        appointment = self.pool.get('oemedical.appointment').browse(self.env.cr, self.env.uid, ids)
        if appointment.invoice_id.id:
            amount_total += appointment.invoice_id.amount_total
            res.append(appointment.invoice_id.id)
        invoice_obj = self.pool.get('account.invoice')
        if appointment.consultations.id == 2 and appointment.patient_id.invoice_id.id:
            res.append(appointment.patient_id.invoice_id.id)
            amount_total += appointment.patient_id.invoice_id.amount_total

        labtest_obj = self.pool.get('oemedical.patient.lab.test')
        labtest_ids = labtest_obj.search(self.env.cr, self.env.uid, [('appointment','=',ids)])
        labtest = labtest_obj.browse(self.env.cr, self.env.uid, labtest_ids)
        for lab in labtest:
            if lab.invoice_id.id:
                res.append(lab.invoice_id.id)
                amount_total += lab.invoice_id.amount_total

        invoice_line_obj = self.pool.get('account.invoice.line')
        invoice_line_ids = invoice_line_obj.search(self.env.cr, self.env.uid, [('invoice_id', 'in', res)])
        invoice_lines = self.pool.get('account.invoice.line').browse(self.env.cr, self.env.uid, invoice_line_ids)
        amount_in_word = self.pool.get('account.voucher').amount_to_text(self.env.cr, self.env.uid, amount_total)
        if total_balance:
            return [{'amount_total': amount_total, 'amount_in_word': amount_in_word}]
        else:
            return invoice_lines
        
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('all_consultation_report.all_consultation_invoice_qweb_report')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'get_investigation_invoice': self._get_investigation_invoice
        }
        return report_obj.render('all_consultation_report.all_consultation_invoice_qweb_report', docargs)
