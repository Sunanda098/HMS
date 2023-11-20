# -*- encoding: utf-8 -*-

from openerp import api, fields, models
from datetime import date, datetime, timedelta
from openerp.exceptions import UserError

class ResPartnerMR(models.Model):
    _inherit = 'res.partner'
    
    is_mr = fields.Boolean('Is MR')
    sex = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Sex')
    codes = fields.Char(size=256, string='Registration ID', help="Medical Representative ID")

    @api.model
    def create(self, values):
        if values.get('codes', '') == '':
            values['codes'] = self.env['ir.sequence'].next_by_code('hms.mr') or ''
        return super(ResPartnerMR, self).create(values)

    @api.multi
    def action_mr_visit(self):
        return {
            'name': ('Mr Visit'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'medical.visit',
            'type': 'ir.actions.act_window',
            'domain': [('medical_representative_id','=',self.id)],
            'context': {
                        'default_medical_representative_id': self.id,
                        },
        }


class MedicalVisit(models.Model):
    _name = 'medical.visit'
    _description = 'Medical Visit'
    _inherit = ['mail.thread', 'ir.needaction_mixin']


    name = fields.Char(size=256, string='Sequence')
    activity_name = fields.Char('Purpose', required="True")
    date_visit = fields.Datetime('Date')
    medical_representative_id = fields.Many2one('res.partner','MR', help="Name of the Mr", domain=[('is_mr','=',True)])
    physician_id = fields.Many2one('hms.physician','Doctor', help="Name of the Doctor")
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('cancelled','Cancelled'),('done','Done')], 'Status', default="draft") 
    remark = fields.Text('Dr Remark')
    product_description = fields.Text('Product Description')

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.visit') or ''
        return super(MedicalVisit, self).create(values)

    @api.multi
    def action_approve(self):
        self.date_visit = datetime.now()
        self.state = 'approved'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def action_cancel(self):
        self.state = 'cancelled'

    @api.multi
    def unlink(self):
        for data in self:
            if data.state in ['done']:
                raise UserError(('You can only delete in draft'))
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

