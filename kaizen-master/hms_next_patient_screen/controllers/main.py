# -*- coding: utf-8 -*-

import babel.dates
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from openerp import http
from openerp import tools, SUPERUSER_ID
from openerp.addons.website.models.website import slug
from openerp.http import request
from openerp.tools.translate import _


class hms_next_patient_screen(http.Controller):
    @http.route(['/next_patient'], type='http', auth="public", website=True)
    def next_patient(self, **kw):
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        app_obj = request.registry['hms.appointment']
        
        one_id = app_obj.search(cr,uid, [('cabin', '=', 'one'),('state', 'in', ['in_consultation','sr_dr','f_x','dressing'])],order='date_start desc', limit=1, context=context)
        two_id = app_obj.search(cr,uid, [('cabin', '=', 'two'),('state', 'in', ['in_consultation','sr_dr','f_x','dressing'])],order='date_start desc', limit=1, context=context)
        three_id = app_obj.search(cr,uid, [('cabin', '=', 'three'),('state', 'in', ['in_consultation','sr_dr','f_x','dressing'])],order='date_start desc', limit=1, context=context)
        four_id = app_obj.search(cr,uid, [('cabin', '=', 'four'),('state', 'in', ['in_consultation','sr_dr','f_x','dressing'])],order='date_start desc', limit=1, context=context)
        
        one = app_obj.browse(cr,uid,one_id,context=context)
        two = app_obj.browse(cr,uid,two_id,context=context)
        three = app_obj.browse(cr,uid,three_id,context=context)
        four = app_obj.browse(cr,uid,four_id,context=context)
        return request.render("hms_next_patient_screen.next_patient_view",{'one':one,'two':two,'three':three,'four':four})

