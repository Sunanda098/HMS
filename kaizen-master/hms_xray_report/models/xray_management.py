# -*- encoding: utf-8 -*-

from openerp import api, fields, models
from datetime import date, datetime, timedelta
from openerp.exceptions import UserError

class XrayInvestigation(models.Model):
    _name = 'xray.investigation'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'X-ray Investigation'

    name = fields.Char(size=256, string='Sequence',required=True, readonly=True, default='New', copy=False)
    investigation_id = fields.Many2one('hms.investigation', string='Investigation', ondelete="restrict")
    patient_id = fields.Many2one('hms.patient', ondelete="restrict", string='Patient', help="Patient whose X-ray to be attached")
    doctor_id = fields.Many2one('hms.physician', ondelete="restrict", string='Doctor', help="Doctor in consultant with the patient")
    date_attachment = fields.Date('Date', readonly="True", default=fields.Datetime.now)
    xray_content = fields.Html('Xray Content')
    investigation_type = fields.Selection([('pathology','Pathology'), ('radiology','Radiology')], string='Type',default="pathology")
    state = fields.Selection([('draft','Draft'),('done','Done')], 'Status', default="draft", track_visibility='onchange') 
    template_id = fields.Many2one('xray.template', ondelete="set null", string="X-ray Template")

    @api.multi
    def action_done(self):
        self.name = self.env['ir.sequence'].next_by_code('xray.investigation')
        self.state = 'done'

    @api.onchange('template_id')
    def onchange_template(self):
        self.xray_content = self.template_id.xray_content

    @api.multi
    def unlink(self):
        for data in self:
            if data.state in ['done']:
                raise UserError(('You can only delete in draft'))
        return super(XrayInvestigation, self).unlink()
        
class XrayTemplate(models.Model):
    _name = 'xray.template'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Xray Template'

    name = fields.Char(size=256, string='Investigation Report')
    xray_content = fields.Text('Xray Content')


class IndimediPatient(models.Model):
    _inherit = 'hms.patient' 

    @api.multi
    def action_open_xray(self):
        return {
            'name': ('X-Ray'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'xray.investigation',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id','=',self.id)],
            'context': {
                        'default_patient_id': self.id,
                        },
        }

class IndimediInvestigation(models.Model):
    _inherit = 'hms.investigation' 

    @api.multi
    def action_open_xray(self):
        return {
            'name': ('X-Ray'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'xray.investigation',
            'type': 'ir.actions.act_window',
            'domain': [('investigation_id','=',self.id)],
            'context': {
                'default_investigation_id': self.id,
                'default_patient_id': self.patient_id.id,
                'default_investigation_type': self.investigation_type,
            },
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
