# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class OeMedicalSpecialty(models.Model):
    _name = 'hms.specialty'

    code = fields.Char(size=256, string='Code')
    name = fields.Char(size=256, string='Specialty', required=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
                       ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
