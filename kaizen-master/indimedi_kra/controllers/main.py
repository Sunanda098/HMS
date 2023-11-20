# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.osv import osv, fields
from openerp.addons.web import http
from openerp.addons.web.http import request
import werkzeug.utils
import simplejson
import base64

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
