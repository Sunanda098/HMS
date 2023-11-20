# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class OeMedicalDirections(models.Model):
    _name = 'hms.directions'

    procedure_id = fields.Many2one('medical.procedure', string='Procedure',required=True)
    comments = fields.Char(size=256, string='Comments')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
