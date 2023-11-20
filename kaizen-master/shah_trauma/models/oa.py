# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime

class Xray(models.Model):
    _name = "oa.xray"
   
    name = fields.Char(string='Xray')

class Hips(models.Model):
    _name = "oa.hip"
   
    name = fields.Char(string='Hips/Spine')

class Advice(models.Model):
    _name = "oa.advice"
   
    name = fields.Char(string='Advice')

class ShahOaNoteTemplate(models.Model):
    _name = "shah.oa.note.template"
    _description = "Shah Oa Note Template"

    val_name = fields.Char("NAME")

class ShahOaNote(models.Model):
    _name = "shah.oa.note"
    _description = "Shah Oa Note"

    val_name = fields.Char("NAME")
    val_one = fields.Char("Left")
    val_two = fields.Char("Right")
    oa_data_id = fields.Many2one('shah.oa','Note')

class ShahOaComplaint(models.Model):
    _name = "shah.oa.complaint.template"
    _description = "Shah Oa Complaint Template"

    val_name = fields.Char("NAME")

class ShahOaComplaint(models.Model):
    _name = "shah.oa.complaint"
    _description = "Shah Oa Complaint"

    val_name = fields.Char("NAME")
    months_left = fields.Char("Left")    
    months_right = fields.Char("Right")   
    oa_complaint_id = fields.Many2one('shah.oa','Note')

class History(models.Model):
    _name = "oa.history"
   
    name = fields.Char(string='History')

class ShahOa(models.Model):
    _name = "shah.oa"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Shah Oa"
    
    name = fields.Char(size=10, string='Name', copy=False)
    inpatient_id = fields.Many2one("hms.appointment", ondelete="cascade", string="Appointment")
    patient_id = fields.Many2one(related="inpatient_id.patient_id", string='Patient')
    date_oa = fields.Datetime('Date', required=True, default=fields.Datetime.now)
    oa_complaint_ids =  fields.One2many('shah.oa.complaint','oa_complaint_id',string='Note', default=lambda self: self.get_complaint_data())
    history_id = fields.Many2one('oa.history', string='History of')
    oa_data_ids =  fields.One2many('shah.oa.note','oa_data_id',string='Note', default=lambda self: self.get_data())
    hip_id =  fields.Many2one('oa.hip', string='Hip/Spine')
    xray_id =  fields.Many2one('oa.xray', string='Xray')
    advice_id = fields.Many2one('oa.advice', string='Advice')
    state = fields.Selection([('draft','Draft'),('done','Done'),('cancel','Cancel')], default="draft", string="State")

    def get_name(self,obj):
        name = []
        if obj.patient_id.first_name:
            name.append(str(obj.patient_id.first_name))
            if obj.patient_id.middel_name:
                name.append(str(obj.patient_id.middel_name[0]))
            if obj.patient_id.last_name:
                name.append(str(obj.patient_id.last_name))
            return ' '.join(name)

    @api.model
    def get_complaint_data(self):
        vals = []
        templates = self.env['shah.oa.complaint.template'].search([])
        for line in templates:
            vals.append((0,0,{
                'val_name':line.val_name,
               }))
        return vals

    @api.model
    def get_data(self):
        vals = []
        templates = self.env['shah.oa.note.template'].search([])
        for line in templates:
            vals.append((0,0,{
                'val_name':line.val_name,
               }))
        return vals

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('shah.oa') or ''
        return super(ShahOa, self).create(values)

    @api.multi
    def button_done(self):
        self.state = 'done'

    @api.multi
    def button_cancel(self):
        self.state = 'cancel'        
    
class Appointment(models.Model):
    _inherit = "hms.appointment"
    
    @api.multi
    def action_oa(self):
        return {
            'name': _(self.name),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'shah.oa',
            'domain': [('inpatient_id','=',self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_inpatient_id': self.id},
        }