# -*- encoding: utf-8 -*-

from openerp import api, fields, models
from datetime import date, datetime, timedelta
from openerp.exceptions import UserError

class CertificateManagement(models.Model):
    _name = 'certificate.management'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Certificate Management'

    name = fields.Char(size=256, string='Sequence',required=True, readonly=True,default='New', copy=False)
    patient_id = fields.Many2one('hms.patient',string='Patient', ondelete="restrict", help="Patient whose certificate to be attached")
    doctor_id = fields.Many2one('hms.physician',string='Doctor', ondelete="restrict", help="Doctor in consultant with the patient")
    date_attachment = fields.Date('Date', readonly="True", default=fields.Datetime.now)
    certificate_content = fields.Text('Certificate Content')
    state = fields.Selection([('draft','Draft'),('done','Done')], 'Status', default="draft", track_visibility='onchange') 
    template_id = fields.Many2one('certificate.template', string="Certificate Template", ondelete="cascade")

    @api.multi
    def action_done(self):
        self.name = self.env['ir.sequence'].next_by_code('certificate.management')
        self.state = 'done'


    @api.onchange('template_id')
    def onchange_template(self):
        self.certificate_content = self.template_id.certificate_content

    @api.multi
    def unlink(self):
        for data in self:
            if data.state in ['done']:
                raise UserError(('You can only delete in draft'))
        return super(CertificateManagement, self).unlink()
       
class CertificateTemplate(models.Model):
    _name = 'certificate.template'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Certificate Template'

    name = fields.Char("Template")
    certificate_content = fields.Text('Certificate Content')

class IndimediPatient(models.Model):
    _inherit = 'hms.patient' 

    @api.multi
    def action_open_certificate(self):
        return {
            'name': ('Certificate'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'certificate.management',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id','=',self.id)],
            'context': {
                'default_patient_id': self.id,
            },
        }
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
