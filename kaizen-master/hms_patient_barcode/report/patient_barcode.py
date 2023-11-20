# # -*- coding: utf-8 -*-

from openerp import api, models

class hms_patient_barcode(models.AbstractModel):
    _name = 'report.hms_patient_barcode.report_patient_barcode'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hms_patient_barcode.report_patient_barcode')
        wizard = self.env['patient.barcode.wizard'].browse(data.get('wizard_id', False))
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(data.get('active_ids', False)),
            'quantity': wizard.quantity,
            'starting_position': wizard.starting_position,
        }
        return report_obj.render('hms_patient_barcode.report_patient_barcode', docargs)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: