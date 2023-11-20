# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime

class ShahSpineNoteTemplate(models.Model):
    _name = "shah.spine.note.template"
    _description = "Shah Spine Note Template"

    val_name = fields.Char("NAME")
    val_selection = fields.Selection([('top','Top'),('bottom','Bottom'),('left','Left'),('right','Right')], string="State") 

class ShahSpineNote(models.Model):
    _name = "shah.spine.note"
    _description = "Shah Spine Note"

    val_name = fields.Char("NAME")
    val = fields.Boolean("Yes/No")
    spine_data_id = fields.Many2one('shah.spine','Note')
    spine_sdata_id = fields.Many2one('shah.spine','Note')
    spine_tdata_id = fields.Many2one('shah.spine','Note')
    spine_fdata_id = fields.Many2one('shah.spine','Note')

class Xray(models.Model):
    _name = "spine.xray"
   
    name = fields.Char(string='Xray')

class Advice(models.Model):
    _name = "spine.advice"
   
    name = fields.Char(string='Advice')

class Mri(models.Model):
    _name = "spine.mri"
   
    name = fields.Char(string='MRI')

class CtScan(models.Model):
    _name = "spine.ctscan"
   
    name = fields.Char(string='CT-Scan')

class Others(models.Model):
    _name = "spine.others"
   
    name = fields.Char(string='Others')

class Diagnosis(models.Model):
    _name = "spine.diagnosis"
   
    name = fields.Char(string='Diagnosis')

class Plan(models.Model):
    _name = "spine.plan"
   
    name = fields.Char(string='Plan')

class ShahSpine(models.Model):
    _name = "shah.spine"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Shah Spine"
    
    name = fields.Char(size=10, string='Name', copy=False)
    inpatient_id = fields.Many2one("hms.appointment", ondelete="cascade", string="Hospitalization")
    patient_id = fields.Many2one(related="inpatient_id.patient_id", string='Patient')
    date_hipjoint = fields.Datetime('Date', required=True, default=fields.Datetime.now)
    chief_complaint_id = fields.Many2one('chief.complaint','Chief Complaint')
    state = fields.Selection([('draft','Draft'),('done','Done'),('cancel','Cancel')], default="draft", string="State")
    spine_data_ids =  fields.One2many('shah.spine.note','spine_data_id',string='Note',default=lambda self: self.get_top())
    spine_sdata_ids =  fields.One2many('shah.spine.note','spine_sdata_id',string='Note',default=lambda self: self.get_left())
    spine_tdata_ids =  fields.One2many('shah.spine.note','spine_tdata_id',string='Note',default=lambda self: self.get_right())
    spine_fdata_ids =  fields.One2many('shah.spine.note','spine_fdata_id',string='Note',default=lambda self: self.get_bottom())
    xray_id =  fields.Many2one('spine.xray', string='Xray')
    advice_id = fields.Many2one('spine.advice', string='Advice')
    mri_id =  fields.Many2one('spine.mri', string='MRI')
    other_id = fields.Many2one('spine.others', string='Others')
    ctscan_id = fields.Many2one('spine.ctscan', string='CT-Scan')
    diagnosis_id = fields.Many2one('spine.diagnosis', string='Diagnosis')
    plan_id = fields.Many2one('spine.plan', string='Plan')    

    @api.model
    def create(self, values):
        if values.get('name', '') == '':
            values['name'] = self.env['ir.sequence'].next_by_code('shah.spine') or ''
        return super(ShahSpine, self).create(values)

    @api.model
    def get_top(self):
        vals = []
        templates = self.env['shah.spine.note.template'].search([('val_selection','=','top')])
        for line in templates:
            vals.append((0,0,{
                'val_name':line.val_name,
               }))
        return vals

    @api.model
    def get_bottom(self):
        vals = []
        templates = self.env['shah.spine.note.template'].search([('val_selection','=','bottom')])
        for line in templates:
            vals.append((0,0,{
                'val_name':line.val_name,
               }))
        return vals

    @api.model
    def get_left(self):
        vals = []
        templates = self.env['shah.spine.note.template'].search([('val_selection','=','left')])
        for line in templates:
            vals.append((0,0,{
                'val_name':line.val_name,
               }))
        return vals

    @api.model
    def get_right(self):
        vals = []
        templates = self.env['shah.spine.note.template'].search([('val_selection','=','right')])
        for line in templates:
            vals.append((0,0,{
                'val_name':line.val_name,
               }))
        return vals

    @api.multi
    def button_done(self):
        self.state = 'done'

    @api.multi
    def button_cancel(self):
        self.state = 'cancel'        
    
class Appointment(models.Model):
    _inherit = "hms.appointment"
    
    @api.multi
    def action_spine(self):
        return {
            'name': _(self.name),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'shah.spine',
            'domain': [('inpatient_id','=',self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_inpatient_id': self.id,'default_patient_id':self.patient_id.id},
        }