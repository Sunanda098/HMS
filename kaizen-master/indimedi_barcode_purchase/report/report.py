# -*- encoding: utf-8 -*-

import base64
from openerp.report import report_sxw
from reportlab.graphics.barcode import createBarcodeDrawing

class barcode_report_parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(barcode_report_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'barcode': self.barcode,
        })

    def barcode(self, type, value, width=600, height=100, humanreadable=0):
        width, height, humanreadable = int(width), int(height), bool(humanreadable)
        barcode_obj = createBarcodeDrawing(
            type, value=value, format='png', width=width, height=height,
            humanReadable = humanreadable
        )
        return base64.encodestring(barcode_obj.asString('png'))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
