# -*- coding: utf-8 -*-

import time
from openerp import api, fields, models


class PatientBarcodeWizard(models.TransientModel):
    _name = 'patient.barcode.wizard'

    @api.one
    def _starting_position(self):
        self.starting_position = (((self.rows-1)*2) + self.columns)-1

    columns = fields.Integer(string="Columns",default="1")
    rows = fields.Integer(string="Rows",default="1")
    quantity = fields.Integer(string="Quantity",default="1")
    starting_position = fields.Integer(compute=_starting_position,string="Position",readonly="True")


    def print_report(self, cr, uid, ids, context=None):
        datas = context
        datas.update({'wizard_id':ids[0], 'ids':ids[0]})
        return self.pool['report'].get_action(cr, uid, context.get('active_ids'), 'hms_patient_barcode.report_patient_barcode', data=datas, context=context)


#    @api.multi
#    def print_report(self):
#        context = self._context or {}
#        return self.pool['report'].get_action('hms_patient_barcode.report_patient_barcode')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
