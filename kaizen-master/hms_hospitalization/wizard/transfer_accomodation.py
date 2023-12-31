# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api
from datetime import datetime
from openerp.exceptions import ValidationError, UserError


class TransferAccomodation(models.TransientModel):
    _name = "transfer.accomodation"

    inpatient_id = fields.Many2one('inpatient.registration', 'Hospitalization', required=True)
    patient_id = fields.Many2one ('hms.patient','Patient', required=True)
    old_department_id = fields.Many2one("hospital.department", "Department")
    old_ward = fields.Many2one ('hospital.ward', 'Ward/Room')
    old_bed = fields.Many2one ('hospital.bed', 'Bed No.')
    new_ward = fields.Many2one ('hospital.ward', 'Ward/Room')
    new_bed = fields.Many2one ('hospital.bed', 'Bed No.')
    new_department_id = fields.Many2one("hospital.department", "Department")

    @api.model
    def default_get(self,fields):
        context = self._context or {}
        res = super(TransferAccomodation, self).default_get(fields)
        hospitalization = self.env['inpatient.registration'].browse(context.get('active_ids', []))
        res.update({
            'inpatient_id': hospitalization.id,
            'old_department_id': hospitalization.department_id.id,
            'patient_id': hospitalization.patient_id.id,
            'new_department_id': hospitalization.department_id.id,
            'old_ward': hospitalization.ward_id.id,
            'old_bed': hospitalization.bed_id.id,
        })
        return res

    @api.multi
    def transfer_accomodation(self):
        context = self._context or {}
        history_obj = self.env['patient.accomodation.history']
        for data in self:
            hist_id = history_obj.search([('inpatient_id','=',data.inpatient_id.id), ('bed_id','=',data.old_bed.id)])
            if data.new_bed and data.new_bed.state != 'free':
                raise ValidationError(_("Bed status not Free!!"))
            hist_id.write({'end_date': datetime.now()})
            data.old_bed.write({'state': 'free'})
            data.new_bed.write({'state': 'reserved'})
            history_obj.create({
                'inpatient_id': data.inpatient_id.id,
                'patient_id': data.patient_id.id,
                'ward_id': data.new_ward.id,
                'bed_id': data.new_bed.id,
                'start_date': datetime.now(),
                'department_id': data.new_department_id.id,
                'type': 'hosp',
            })
            data.inpatient_id.write({
                'departme nt_id': data.new_department_id.id,
                'ward_id': data.new_ward.id,
                'bed_id': data.new_bed.id,
            })
        return {'type': 'ir.actions.act_window_close'}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
