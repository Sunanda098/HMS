# -*- coding: utf-8 -*-

import time
from openerp.report import report_sxw
from datetime import datetime, timedelta

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
