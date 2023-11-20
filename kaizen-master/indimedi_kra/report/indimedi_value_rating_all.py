# -*- coding: utf-8 -*-

import time
from openerp.report import report_sxw
from datetime import datetime, timedelta

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_value_rating':self.get_value_rating,
        })
        
    def get_value_rating(self, obj, context=None):
        value_obj = self.pool.get('value.rating')
        search_ids = value_obj.search(self.cr, self.uid, [('month', '>=', obj.month_from), ('month', '<=', obj.month_to), ('year', '=', obj.year.id), ('employee_id', '=', obj.employee_id.id)])
        values_ratings = value_obj.browse(self.cr, self.uid, search_ids)
        return values_ratings


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
