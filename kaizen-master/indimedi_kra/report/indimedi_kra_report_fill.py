# -*- coding: utf-8 -*-

import time
from openerp.report import report_sxw
from datetime import datetime, timedelta

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_total':self._get_total,
        })

    def _get_total(self, obj, context=None):
        gpa = 0.0
        final_score = 0.0
        for q in obj.kra_question_ids:
            final_score += (q.weightage * q.manager_rating) / 10
        gpa = final_score / 20
        return {'gpa':gpa, 'final_score':final_score}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
