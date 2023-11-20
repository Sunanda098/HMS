# -*- encoding: utf-8 -*-
from openerp import api, fields, models, SUPERUSER_ID, _


def isodd(x):
    return bool(x % 2)

class IndimediPatient(models.Model):
    _inherit = "hms.patient"

    barcode = fields.Char(string='EAN13 Barcode', size=13, help="International Article Number used for Patient identification.")
    generate_ean = fields.Boolean(string='Generate Ean13', default=False, copy=False)

    _sql_constraints = [('ean13_uniq', 'UNIQUE(barcode)', 'Ean13 must be unique!'),]

    @api.onchange('generate_ean')
    def onchange_generate_ean(self):
        if self.generate_ean:
            ean = self.env['ir.sequence'].next_by_code('patient.ean13.code') or '/'
            if len(ean) > 12:
                raise orm.except_orm(_("Configuration Error!"),
                     _("There next sequence is upper than 12 characters. This can't work."
                       "You will have to redefine the sequence or create a new one"))
            else:
                ean = (len(ean[0:6]) == 6 and ean[0:6] or ean[0:6].ljust(6,'0')) + ean[6:].rjust(6,'0')
            sum = 0
            for i in range(12):
                if isodd(i):
                    sum += 3 * int(ean[i])
                else:
                    sum += int(ean[i])
            key = (10 - sum % 10) % 10
            ean13 = ean + str(key)
            self.barcode = ean13

class Appointment(models.Model):
    _inherit = 'hms.appointment'

    get_patient_ean = fields.Char(string='Add Patient', size=13, help="Read a Barcode to set patient detail.")

    @api.onchange('get_patient_ean')
    def onchange_patient_ean(self):
        if not self.get_patient_ean:
            return
        patient_id = self.env['hms.patient'].search([('barcode','=',self.get_patient_ean)], limit=1)
        if patient_id:
            self.patient_id = patient_id.id
        else:
            warning = {'title': _('Warning!'),
                'message': _("There is no patient with Barcode: %s") % (self.get_patient_ean),
            }
            self.get_patient_ean = False
            return {'warning':warning}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
