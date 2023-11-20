# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime

class ChiefComplaint(models.Model):
    _name = "chief.complaint"
   
    name = fields.Char(string='Chief Complaint')

class History(models.Model):
    _name = "shah.history"
   
    name = fields.Char(string='History')

class Gait(models.Model):
    _name = "shah.gait"
   
    name = fields.Char(string='Gait')

class Limb(models.Model):
    _name = "shah.limb"
   
    name = fields.Char(string='Limb Length')

class Xray(models.Model):
    _name = "hipjoint.xray"
   
    name = fields.Char(string='Xray')

class Advice(models.Model):
    _name = "hipjoint.advice"
   
    name = fields.Char(string='Advice')

class ShahHipNoteTemplate(models.Model):
    _name = "shah.hip.note.template"
    _description = "Shah Hip Note Template"

    val_name = fields.Char("NAME")
    val_one = fields.Char("Left")
    val_two = fields.Char("Right")

class ShahHipNote(models.Model):
    _name = "shah.hip.note"
    _description = "Shah Hip Note"

    val_name = fields.Char("NAME")
    val_one = fields.Char("Left")
    val_two = fields.Char("Right")
    hip_data_id = fields.Many2one('shah.hipjoint','Note')

class ShahHipjoint(models.Model):
    _name = "shah.hipjoint"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Shah Hip joint"
    
    name = fields.Char(size=10, string='Name', copy=False)
    inpatient_id = fields.Many2one("hms.appointment", ondelete="cascade", string="Appointment")
    patient_id = fields.Many2one(related="inpatient_id.patient_id", string='Patient')
    date_hipjoint = fields.Datetime('Date', required=True, default=fields.Datetime.now)
    chief_complaint_id = fields.Many2one('chief.complaint','Chief Complaint')
    history_id = fields.Many2one('shah.history', string='History of Loss')
    gait =  fields.Many2one('shah.gait', string='Gait')
    limb = fields.Many2one('shah.limb', string='Limb')
    discrepancy = fields.Char('Discrepancy')
    deformaty_left = fields.Char('Deformatry')
    deformaty_right = fields.Char('Deformatry')
    hip_data_ids =  fields.One2many('shah.hip.note','hip_data_id',string='Note', default=lambda self: self.get_data())
    xray_id =  fields.Many2one('hipjoint.xray', string='Xray')
    advice_id = fields.Many2one('hipjoint.advice', string='Advice')
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
    def get_data(self):
        vals = []
        templates = self.env['shah.hip.note.template'].search([])
        for line in templates:
            vals.append((0,0,{
                'val_name':line.val_name,
                'val_one':line.val_one,
                'val_two':line.val_two,
               }))
        return vals

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('shah.hipjoint') or ''
        return super(ShahHipjoint, self).create(values)

    @api.multi
    def button_done(self):
        self.state = 'done'

    @api.multi
    def button_cancel(self):
        self.state = 'cancel'        
    
class Appointment(models.Model):
    _inherit = "hms.appointment"
    
    @api.multi
    def action_hipjoint(self):
        return {
            'name': _(self.name),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'shah.hipjoint',
            'domain': [('inpatient_id','=',self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_inpatient_id': self.id,'default_patient_id':self.patient_id.id},
        }
