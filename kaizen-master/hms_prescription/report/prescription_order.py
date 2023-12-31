import time
from openerp.report import report_sxw


class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(order, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.patient.prescription.order', 'prescription.order', 'addons/Prescription/report/prescription_order.rml', parser=order, header=False)
