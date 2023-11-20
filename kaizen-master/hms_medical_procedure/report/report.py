# # -*- coding: utf-8 -*-


from openerp import api, models

class OppReport(models.AbstractModel):
    _name = 'report.hms_medical_procedure.oop_discharge_summary'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hms_medical_procedure.oop_discharge_summary')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
        }
        return report_obj.render('hms_medical_procedure.oop_discharge_summary', docargs)

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
