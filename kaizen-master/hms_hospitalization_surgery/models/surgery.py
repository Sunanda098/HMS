 # -*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import datetime, date, timedelta
import openerp.addons.decimal_precision as dp

#Pre Operative Checklist
class PreOpetativeCheckListTemplate(models.Model):
    _name="pre.operative.check.list.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")

class PreOpetativeCheckList(models.Model):
    _name="pre.operative.check.list"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Done", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Surgery')

class PreoperativeInvestigationTemplate(models.Model):
    _name = 'preoperative.investigation.template'

    name = fields.Char(string="Investigation")

class PreoperativeInformationTemplate(models.Model):
    _name = 'preoperative.information.template'

    name = fields.Char(string="Content")

class IndimediConsumableLine(models.Model):
    _name = "consumable.line"
    _rec_name = 'name'
    #Used Fields in View    
    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', ondelete="cascade", string='Consumable')
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', help='Amount of medication (eg, 250 mg) per dose')
    qty = fields.Float(string='Quantity')
    active_component_ids = fields.Many2many('active.comp','consume_line_comp_rel','consume_id','line_id',string='Active Component')
    form = fields.Many2one('drug.form', string='Form', help='Drug form, such as tablet or gel')
    dose = fields.Float(string='Dosage', digits=(16, 2),help="Amount of medication (eg, 250 mg) per dose")
    common_dosage = fields.Many2one('medication.dosage', ondelete="cascade", string='Frequency', help='Drug form, such as tablet or gel')
    #Link with  surgery
    line_id = fields.Many2one('hms_surgery', ondelete="cascade", string='Surgery')
    #Link with hospitalzation 
    # inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Surgery')
    
    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.product_uom = self.product_id.uom_id.id

class IndimediMedicamentLine(models.Model):
    _name = "medicament.line"
    _rec_name = 'name'
    
    product_id = fields.Many2one('product.template',index=True, ondelete="cascade", string='Medicine Name')
    name = fields.Char(string='Name')
    medicine_uom = fields.Many2one('product.uom', string='Unit', help='Amount of medication (eg, 250 mg) per dose')
    qty = fields.Float(string='Quantity',default=1.0)
    active_component_ids = fields.Many2many('active.comp','medica_line_comp_rel','medica_id','line_id',string='Active Component')
    form = fields.Many2one('drug.form', ondelete="cascade", string='Form', help='Drug form, such as tablet or gel')
    dose = fields.Float(string='Dosage', digits=(16, 2) ,help="Amount of medication (eg, 250 mg) per dose")
    common_dosage = fields.Many2one('medication.dosage', ondelete="cascade", string='Frequency', help='Drug form, such as tablet or gel')    
    line_id = fields.Many2one('hms_surgery', ondelete="cascade", string='Surgery')
    # inpatient_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Inpatient')
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Surgery')
    dosage_ml = fields.Float(string='Days', help='Dosage')
    route_ml = fields.Selection([('iv','IV'),('im','IM'),('sc','SC')], string="Route")
    common_dosage_ml = fields.Many2one('medication.dosage', ondelete='cascade', string='Frequency', help='Drug form, such as tablet or gel')
    t1_ml = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T1")
    t2_ml = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T2")
    t3_ml = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T3")
    t4_ml = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T4")
    t5_ml = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T5")
    t6_ml = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T6")


    #Todo After Presciption
    @api.onchange('common_dosage_ml','dosage_ml')
    def onchange_dosage_days(self):
        self.qty = float(self.common_dosage_ml.code) * int(self.dosage_ml) or 1

    @api.onchange('product_id')
    def onchange_product_id(self):       
        if self.product_id:
            self.form = self.product_id.form.id
            # 'active_component_ids': [(6, 0, [x.id for x in prod_id.active_component_ids])],

class MedicationSchedule(models.Model):
    _name = "medication.schedule"

    line_id = fields.Many2one('hms_surgery', ondelete='cascade', string='Surgery')
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Surgery')
    # inpatient_id = fields.Many2one('inpatient.registration', ondelete='restrict', string='Inpatient')
    product_id = fields.Many2one('product.template', ondelete='cascade', string='Medicine Name')
    day = fields.Selection([('1','Day 1'),('1','Day 1'),('3','Day 3'),('4','Day 4'),('5','Day 5'),('6','Day 6'),('7','Day 7'),('8','Day 8'),('9','Day 9'),('10','Day 10')],string='Day',default='1')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('missed', 'Missed'),
        ('delayed', 'Delayed'),
        ('delivered', 'Delivered'),
        ], string='Status', default='pending')
    time = fields.Char(string='Time')
    instruction = fields.Char(string='Instruction')
    remarks = fields.Char(string='Remarks')
    actual_time = fields.Datetime(string='Actual Time')
    administered_by = fields.Many2one('res.users', ondelete='cascade', string='Administered by')
    form = fields.Many2one('drug.form', ondelete='cascade', string='Drug Form', help='Drug form, such as tablet or gel')
    common_dosage = fields.Many2one('medication.dosage', ondelete='cascade', string='Frequency', help='Drug form, such as tablet or gel')
    quantity = fields.Float(string='Units',default=1.0)
    dose = fields.Float(string='Dosage', digits=(16, 2) ,help="Amount of medication (eg, 250 mg) per dose")
    dose_unit = fields.Many2one('product.uom', string='Dosage Unit', help='Amount of medication (eg, 250 mg) per dose')
    
    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.product_uom = self.product_id.uom_id.id


class InstructionList(models.Model):
    _name = 'instruction.list'
    name = fields.Char(string='Name', required=True)


class InstructionSet(models.Model):
    _name = "instruction.set"

    instruction_list_id = fields.Many2one('instruction.list', ondelete="restrict", string='Instruction Id')
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Instruction')
    instruction_done = fields.Boolean(string="Done",default=False)
    instruction_time_ins = fields.Char(string="Time", readonly=True)
    
    @api.onchange('instruction_done')
    def onchange_done(self):
        if self.instruction_done:
            self.instruction_time_ins = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

class IpsFluid(models.Model):
    _name = 'ips.fluid'
    name = fields.Char(string='Name')

class IpFluid(models.Model):
    _name = "ip.fluid"

    fluid_id = fields.Many2one('ips.fluid', ondelete="cascade", string='I/V Fluids',)
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Inpatient')
    rate = fields.Char(string='Rate')
    quantity = fields.Char(string='Quantity')
    ####start kaizen customization####
    iv_id = fields.Many2one('product.template', ondelete="cascade", string='Name', required=True)
    dosage_iv = fields.Float(string='Dosage', help='Dosage')
    route_iv = fields.Selection([('iv','IV'),('im','IM'),('sc','SC')], string="Route")
    common_dosage_iv = fields.Many2one('medication.dosage', ondelete='cascade', string='Frequency', help='Drug form, such as tablet or gel')
    t1_iv = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T1")
    t2_iv = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T2")
    t3_iv = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T3")
    t4_iv = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T4")
    t5_iv = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T5")
    t6_iv = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T6")
    ####end kaizen customization####

class AntibioticAnalogesis(models.Model):
    _name = "antibiotic.analogesis"
    
    anti_id = fields.Many2one('product.template', ondelete="cascade", string='Name', required=True)
    #antibiotics_id = fields.Many2one('product.template',string='Antibiotic and Analogesis')
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Inpatient')
    
    ########start kaizen customization#######
    dosage_anti = fields.Float(string='Dosage', help='Dosage')
    route_anti = fields.Selection([('iv','IV'),('im','IM'),('sc','SC')], string="Route")
    common_dosage_anti = fields.Many2one('medication.dosage', ondelete='cascade', string='Frequency', help='Drug form, such as tablet or gel')
    t1_anti = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T1")
    t2_anti = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T2")
    t3_anti = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T3")
    t4_anti = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T4")
    t5_anti = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T5")
    t6_anti = fields.Selection([('1','1AM'),
                                ('2','2AM'),
                                ('3','3AM'),
                                ('4','4AM'),
                                ('5','5AM'),
                                ('6','6AM'),
                                ('7','7AM'),
                                ('8','8AM'),
                                ('9','9AM'),
                                ('10','10AM'),
                                ('11','11AM'),
                                ('12','12AM'),
                                ('13','1PM'),
                                ('14','2PM'),
                                ('15','3PM'),
                                ('16','4PM'),
                                ('17','5PM'),
                                ('18','6PM'),
                                ('19','7PM'),
                                ('20','8PM'),
                                ('21','9PM'),
                                ('22','10PM'),
                                ('23','11PM'),
                                ('24','12PM')],string="T6")
    ########end kaizen customization

    sos = fields.Boolean(string="SOS")
    t1 = fields.Integer(string="T1")
    b1 = fields.Boolean(string="C1")
    time1 = fields.Char(string="Time")
    t2 = fields.Integer(string="T2")
    b2 = fields.Boolean(string="C2")
    time2 = fields.Char(string="Time")
    t3 = fields.Integer(string="T3")
    b3 = fields.Boolean(string="C3")
    time3 = fields.Char(string="Time")
    t4 = fields.Integer(string="T4")
    b4 = fields.Boolean(string="C4")
    time4 = fields.Char(string="Time")

    @api.one
    @api.constrains('t1', 't2', 't3', 't4')
    def _check_my_field(self):
        if (self.t1 < 0 or self.t1 > 24) or (self.t2 < 0 or self.t2 > 24) or (self.t3 < 0 or self.t3 > 24) or (self.t4 < 0 or self.t4 > 24):
            raise ValidationError(_("Enter Value Of Time Between  0 to 24 hrs"))

    @api.onchange('b1')
    def onchange_b1(self):
        if self.b1:
            self.time1 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b2')
    def onchange_b2(self):
        if self.b2:
            self.time2 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b3')
    def onchange_b3(self):
        if self.b3:
            self.time3 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b4')
    def onchange_b4(self):
        if self.b4:
           self.time4 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

class MiscellaneousDrugs(models.Model):
    _name = "miscellaneous.drugs"

    misc_id = fields.Many2one('product.template', ondelete="cascade", string='Miscellaneous Drugs', required=True)
    # miscellaneouss_id = fields.Many2one('product.template', string='Miscellaneous Drugs')
    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Inpatient')
    sos = fields.Boolean(string="SOS")
    t5 = fields.Integer(string="T1")
    b5 = fields.Boolean(string="C1")
    time5 = fields.Char(string="Time")
    t6 = fields.Integer(string="T2")
    b6 = fields.Boolean(string="C2")
    time6 = fields.Char(string="Time")
    t7 = fields.Integer(string="T3")
    b7 = fields.Boolean(string="C3")
    time7 = fields.Char(string="Time")
    t8 = fields.Integer(string="T4")
    b8 = fields.Boolean(string="C4")
    time8 = fields.Char(string="Time")
    
    @api.one
    @api.constrains('t5', 't6', 't7', 't8', 't9')
    def _check_my_field2(self):
        if (self.t5 < 0 or self.t5 > 24) or (self.t6 < 0 or self.t6 > 24) or (self.t7 < 0 or self.t7 > 24) or (self.t8 < 0 or self.t8 > 24):
            raise ValidationError(_("Enter Value Of Time Between  0 to 24 hrs"))

    @api.onchange('b5')
    def onchange_b5(self):
        if self.b5:
            self.time5 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b6')
    def onchange_b6(self):
        if self.b6:
            self.time6 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b7')
    def onchange_b7(self):
        if self.b7:
            self.time7 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")

    @api.onchange('b8')
    def onchange_b8(self):
        if self.b8:
            self.time8 = (datetime.now()+timedelta(hours=5,minutes=30)).strftime("%H:%M")


class IndimediSurgery(models.Model):
    _inherit = "hms_surgery"
    _description = "Surgery"
    
    consumable_line = fields.One2many('consumable.line', 'line_id', string='Consumable Line')
    medicament_line = fields.One2many('medicament.line', 'surgery_id', string='Medicament Line')
    medicaments_id = fields.One2many('medication.schedule', 'surgery_id', string='Medication (24 Hours post-Surgery)')
    medicaments_plan_id = fields.One2many('medication.schedule', 'surgery_id', string='Medication Plan (Post 24 Hour Medication)')
    medication_schedule_line = fields.One2many('medication.schedule', 'surgery_id', string='Medication Schedule')

####RBK####
class IndimediIPDOpnoteFellow(models.Model):
    _name = "indimedi.ipd.discharge.fellow"
    _description = "IPD Opnote Fellow"
    
    name = fields.Char(string='Fellow',required=True)


class HmsIncision(models.Model):
    _name = 'hms.incision'
        
    name = fields.Char('Incision')

class HmsApproach(models.Model):
    _name = 'hms.approach'

    name = fields.Char('Approach')


class IndimediHospitalOr(models.Model):
    _name = 'indimedi.hospital.or'

    patient_id = fields.Many2one('hms.patient', ondelete="restrict", string='Patient')
    hospitalize_id = fields.Many2one('inpatient.registration', ondelete="restrict", string='Hosp Id') 
    doctor_id = fields.Many2one('hms.physician', string='Doctor', ondelete="restrict")
    start_date = fields.Datetime(string='Start Date',default = fields.Datetime.now)
    end_date = fields.Datetime(string='End Date',default = fields.Datetime.now)
    building = fields.Many2one('hospital.building', string='Department', select=True, ondelete="restrict")
    name = fields.Char(size=256, string='Name', required=True, help='Name of the Operating Room')
    institution = fields.Many2one('res.partner', string='Institution', help='Medical Center', ondelete="restrict")
    extra_info = fields.Text(string='Extra Info')
    telephone_number = fields.Integer(string='Telephone Number',help='Telephone number / Extension')
    state = fields.Selection([
        ('free', 'Free'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('na', 'Not available')], string=' Current Status')

    _sql_constraints = [('name_uniq', 'UNIQUE(name)', 'Name must be unique!')]


class IndimediHospitalBuilding(models.Model):
    _name = 'hospital.building'

    code = fields.Char(size=8, string='Code')
    institution = fields.Many2one('res.partner', ondelete="restrict", string='Institution',help='Medical Center')
    name = fields.Char(size=256, string='Name', required=True,help='Name of the building within the institution')
    extra_info = fields.Text(string='Extra Info')


class OemedicalReason(models.Model):
    _name= "hms.reason"
    
    name = fields.Char(string="Reason")


class HmsImplant(models.Model):
    _name = 'hms.implant'

    name = fields.Char('Implant')


class ImplantCompany(models.Model):
    _name = 'implant.company'

    name = fields.Char('Company Name')


class ImplantSize(models.Model):
    _name = 'implant.size'

    name = fields.Char('Implant Size')


class IndimediIPDOpnoteClosure(models.Model):
    _name = "indimedi.ipd.opnote.closure"
    _description = "IPD Closure"
    
    name = fields.Char(string='Closure',required=True)


class IndimediIPDOpnoteDrainage(models.Model):
    _name = "indimedi.ipd.opnote.drainage"
    _description = "IPD Drainage"
    
    name = fields.Char(string='Drainage',required=True)


class IndimediIPDOpnoteHistopathology(models.Model):
    _name = "indimedi.ipd.opnote.histopathology"
    _description = "IPD OT  Note"
    
    name = fields.Char(string='Histopathology',required=True)


class IndimediIPDOpnoteComments(models.Model):
    _name = "indimedi.ipd.opnote.comments"
    _description = "IPD Opnote Comments"
    
    name = fields.Char(string='Comments',required=True)


class OpOperativeMorbidity(models.Model):
    _name = 'op.operative.morbidity'

    op_morbidity = fields.Many2one('op.surgery.morbidity',string="Morbidity")
    op_grade = fields.Many2one('op.surgery.grade',string="Grade")
    op_management = fields.Char(string='Management')
    op_outcome = fields.Many2one('op.surgery.outcome',string='Outcome')
    op_operative_morbidity_id = fields.Many2one('inpatient.registration', string="Hospitalization")


class OpSurgeryMorbidity(models.Model):
    _name = 'op.surgery.morbidity'
    _rec_name = 'name'

    name = fields.Char('Morbidity')

class OpSurgeryGrade(models.Model):
    _name = 'op.surgery.grade'
    _rec_name = 'name'

    name = fields.Char('Morbidity')

class OpSurgeryOutcome(models.Model):
    _name = 'op.surgery.outcome'
    _rec_name = 'name'

    name = fields.Char('Morbidity')


class PastHistoryHospitalization(models.Model):
    _name = 'past.history.hospitalization'

    cause = fields.Char(string="Cause")
    past_hos_duration = fields.Char(string="Duration")
    past_history_hosp_id = fields.Many2one('inpatient.registration')


class PasthistoryOperation(models.Model):
    _name = 'past.history.operation'

    past_op = fields.Char(string="Operation")
    past_op_yr = fields.Integer(string="Year")
    past_history_op_id = fields.Many2one('inpatient.registration')


class AnesthesiaPersonalHistory(models.Model):
    _name = 'anesthesia.personal.history'

    ah_name = fields.Many2one('anesthesia.personhis','Name')
    duration =fields.Char('Duration')
    frequency = fields.Char('Frequency')
    anesthesia_personal_history_id = fields.Many2one('inpatient.registration','Anesthesia')

class AnesthesiaPerHis(models.Model):
    _name = 'anesthesia.personhis'

    name = fields.Char('Name')

class AnesthesiPreOperativeInstructions(models.Model):
    _name = 'anesthesia.pre.operative.instructions'
    
    name = fields.Char('Name')
    anesthesia_pre_operative_instructions_id = fields.Many2one('inpatient.registration','Anesthesia')


class OtherInvestigations(models.Model):
    _name = 'other.investigations'

    name = fields.Char(string="Name")
    other_investigations_id = fields.Many2one('inpatient.registration','Anesthesia')


class IntraOpVital(models.Model):
    _name= 'intra.op.vital'

    inpatient_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    io_time = fields.Datetime(string="Time", default=fields.datetime.now())
    io_pulse = fields.Char(string="Pulse")
    io_bp = fields.Char(string="BP")
    io_spo2 = fields.Char(string="SPO2")
    io_etco2 = fields.Char(string="ETCO2")
    io_temp = fields.Char(string="Temp")
    io_pap  = fields.Char(string="PAP")
    io_cvp  = fields.Char(string="Cvp")
    io_urine  = fields.Char(string="Urine")
    io_blood_loss  = fields.Char(string="Blood Loss")
    io_rl_dns_ns_d5  = fields.Char(string="RL/DNS/NS/D5")
    io_colloids  = fields.Char(string="Colloids")
    io_blood_prod  = fields.Char(string="Blood Products")
    io_intropes  = fields.Char(string="Inotropes")
    io_atracurium  = fields.Char(string="Atracurium/Rocuronium")
    io_dexmeditonidine  = fields.Char(string="Dexmeditonidine")
    io_others  = fields.Char(string="Others")


class SpinalDrug(models.Model):
    _name = 'spinal.drug'

    inpatient_id = fields.Many2one('inpatient.registration', string="Hospitalization")
    spinal_drug = fields.Char(string="Drug")
    spinal_dose = fields.Char(string="Dose")
    spinal_time = fields.Char(string="Time")


class PostAnsAdvice(models.Model):
    _name = 'post.ans.advice'

    inpatient_id = fields.Many2one("inpatient.registration", string="Hospitalization")
    advice_list_id = fields.Many2one('post.advice.ans.list',string="Advice")
    advice_post_ans = fields.Char(string="Description")

class PostAdviceAnsList(models.Model):
    _name = 'post.advice.ans.list'

    name = fields.Char(string="Advice", required=True)

class PostAdviceAnsList(models.Model):
   _name = 'post.advice.ans.list'

   name = fields.Char(string="Advice", required=True)


class IvlineRa(models.Model):
    _name = 'ivline.ra'

    name = fields.Char(string="IV Line RA", required=True)

class IvlineLa(models.Model):
    _name = 'ivline.la'

    name = fields.Char(string="IV Line LA", required=True)


class PatientAccomodationHistory(models.Model):
    _inherit = 'patient.accomodation.history'

    surgery_id = fields.Many2one('inpatient.registration.surgery', string='Surgery')


class SurgeryReg(models.Model):
    _name = 'inpatient.registration.surgery'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def _default_fellow(self):
       vals = []
       checklists = self.env['inpatient.checklist.fellow.template'].search([])
       for checklist in checklists:
           vals.append((0, 0, {
               'name': checklist.name,
               'remark': checklist.remark,
           }))
       return vals

    @api.model
    def _default_anesthetist(self):
       vals = []
       checklists = self.env['inpatient.checklist.anesthetist.template'].search([])
       for checklist in checklists:
           vals.append((0, 0, {
               'name': checklist.name,
               'remark': checklist.remark,
           }))
       return vals

    @api.model
    def _default_operating_surgeon(self):
       vals = []
       checklists = self.env['inpatient.checklist.operating.surgeon.template'].search([])
       for checklist in checklists:
           vals.append((0, 0, {
               'name': checklist.name,
               'remark': checklist.remark,
           }))
       return vals

    @api.model
    def _default_scrub_nurse(self):
       vals = []
       checklists = self.env['inpatient.checklist.scrub.nurse.template'].search([])
       for checklist in checklists:
           vals.append((0, 0, {
               'name': checklist.name,
               'remark': checklist.remark,
           }))
       return vals

    @api.model
    def _default_otincharge(self):
       vals = []
       checklists = self.env['inpatient.checklist.otincharge.template'].search([])
       for checklist in checklists:
           vals.append((0, 0, {
               'name': checklist.name,
               'remark': checklist.remark,
           }))
       return vals

    @api.model
    def _default_recovery(self):
       vals = []
       checklists = self.env['inpatient.checklist.recovery.checklist.template'].search([])
       for checklist in checklists:
           vals.append((0, 0, {
               'name': checklist.name,
               'remark': checklist.remark,
           }))
       return vals

    @api.model
    def _default_prechecklist(self):
        vals = []
        prechecklists = self.env['pre.operative.check.list.template'].search([])
        for prechecklist in prechecklists:
            vals.append((0,0,{
                'name': prechecklist.name,
                'remark': prechecklist.remark,
            }))
        return vals

    @api.model
    def _default_preopinvchecklist(self):
        vals = []
        preopinvchecklists = self.env['preoperative.investigation.template'].search([])
        for preopinvchecklists in preopinvchecklists:
            vals.append((0,0,{
                'name': preopinvchecklists.name,
            }))
        return vals

    @api.model
    def _default_preopinfochecklist(self):
        vals = []
        preopinfochecklists = self.env['preoperative.information.template'].search([])
        for preopinfochecklists in preopinfochecklists:
            vals.append((0,0,{
                'name': preopinfochecklists.name,
            }))
        return vals

    name = fields.Char(string='Surgery #', size=128, copy=False)
    image = fields.Binary(related='patient_id.image',string='Image', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),('confirm', 'Confirmed'),
        ('progress', 'Progress'),('cancel', 'Cancelled'),
        ('done', 'Done')], string='Status', default='confirm', track_visibility='always')
    inpatient_id = fields.Many2one('inpatient.registration', string="Hospitalization", required=True, track_visibility='always')    
    patient_id = fields.Many2one(related='inpatient_id.patient_id', string='Patient', track_visibility='always', readonly=True)
    mobile = fields.Char(related='patient_id.mobile', string='Mobile', readonly=True)
    appointment_id = fields.Many2one(related='inpatient_id.appointment_id', string='Appointment', readonly=True)
    hospitalization_date = fields.Datetime(related='inpatient_id.hospitalization_date', string='Date of Admission', readonly=True)
    company_id = fields.Many2one('res.company', string='Institution', default=lambda self: self.env.user.company_id.id, readonly=True)
    department_id = fields.Many2one(related='patient_id.department_id', ondelete="restrict", string='Department', readonly=True)
    primary_physician = fields.Many2one(related='inpatient_id.primary_physician', string='Consultant Incharge', readonly=True)
    attending_physician_ids = fields.Many2many(related='inpatient_id.attending_physician_ids', string='Attending Physician', readonly=True)
    relative_name = fields.Char(related='inpatient_id.relative_name', string="Relative Name", readonly=True)
    relative_with_patient = fields.Char(related='inpatient_id.relative_with_patient', string="Relation with Patient", readonly=True)
    relative_m_no = fields.Char(related='inpatient_id.relative_number', string='Relative M. No', readonly=True)
    mlc = fields.Boolean(related='inpatient_id.mlc', string='MLC')
    ward_id = fields.Many2one('hospital.ward', string='Ward/Room', track_visibility='always')
    bed_id = fields.Many2one ('hospital.bed', string='Bed No.', track_visibility='always')
    admission_type = fields.Selection([
        ('routine','Routine'),
        ('lithotripsy', 'Lithotripsy'),
        ('elective','Elective'),
        ('urgent','Urgent'),
        ('emergency','Emergency')], related='inpatient_id.admission_type', string='Admission type', readonly=True)
    admission_reason = fields.Many2one(related='inpatient_id.admission_reason', string='Reason for Admission', help="Reason for Admission", readonly=True)
    discharge_date = fields.Datetime(related='inpatient_id.discharge_date', string='Date of Discharge', readonly=True)
    ##Surgery
    pre_operative_checklist_ids = fields.One2many('pre.operative.check.list', 'surgery_id', string='Pre-Operative Checklist', default=lambda self: self._default_prechecklist())
    consumable_line = fields.One2many('consumable.line', 'surgery_id', string='Consumable Line')
    medicament_line = fields.One2many('medicament.line', 'surgery_id',string='Medicament Line')
    post_instruction_ids = fields.One2many('instruction.set', 'surgery_id', string='Instruction')
    fluid_ids = fields.One2many('ip.fluid', 'surgery_id', string='I/V Fluids')
    antibiotic_ids = fields.One2many('antibiotic.analogesis', 'surgery_id', string='Antibiotic & Analgesics')
    miscellaneous_ids = fields.One2many('miscellaneous.drugs', 'surgery_id', string='Miscellaneous Drugs')
    special_precautions_id = fields.Text(string="Supportive Drugs")
    ###
    ##OperativeNotes#RBK
    surgery_names = fields.Many2many('hms_surgery','hosp_patient_surgery_names','hosp_id','surgery_id', ondelete="restrict", string='Surgery')
    surgery_notes = fields.Text(string='Surgery Note')
    user_id = fields.Many2one('res.users', string='Anesthetist', ondelete="set null", help='Anesthetist data of the patient',domain=[('is_anesthetist','=',True)])
    anaesthesia_id = fields.Many2one('anaesthesia', ondelete="set null", string="Anaesthesia")
    start_date = fields.Datetime(string='Surgery Date')
    end_date = fields.Datetime(string='End Date')
    duration = fields.Char(string="Duration (in mins)", compute='_time_count')

    fellow = fields.Many2many('indimedi.ipd.discharge.fellow','hosp_surg_id','hosp_fellow_id','fellow_id',ondelete="cascade", string="Fellow")
    side = fields.Selection([('left','Left'),('right','Right'),('other','Other')],string="Side")
    iitv = fields.Char(string="IITV")
    position = fields.Char(string="Position")
    incision = fields.Many2one('hms.incision', string='Incision')
    approach = fields.Many2one('hms.approach', string="Approach")
    findings = fields.Text(string="Findings")
    procedure = fields.Text(string="Procedure")
    co_morbidity = fields.Many2many('hms.diseases','rel_surgery_patient_co_morbidity','surgery_id','co_morbidity', string="Co Morbidity")
    allergy = fields.Char(string="Allergy")
    mortality = fields.Boolean(string="Mortality")
    morbidity_check = fields.Boolean('Morbidity')
    sur_department_id = fields.Many2one(related='patient_id.department_id', ondelete="restrict", string='Department')
    hospital_ot = fields.Many2one('indimedi.hospital.or', ondelete="restrict", string='Operation Theatre')
    primary_physician_ids = fields.Many2many('hms.physician','hosp_pri_doc_rel','hosp_id','doc_id',string='Primary Surgeons')
    assisting_surgeons = fields.Many2many('hms.physician','hosp_doc_rel','hosp_id','doc_id',string='Assisting Surgeons')
    scrub_nurse = fields.Many2one('res.users', ondelete="set null", string='Scrub Nurse',domain=[('is_nurse','=',True)])
    reason_id = fields.Many2one('hms.reason', ondelete="cascade", string='Reason')
    implant_name = fields.Many2one('hms.implant', ondelete="cascade", string='Implant')
    implant_company = fields.Many2one('implant.company', ondelete="cascade", string='Implant Company')
    implant_size = fields.Many2one('implant.size', string="Implant Size")
    closure = fields.Many2one('indimedi.ipd.opnote.closure',ondelete="cascade", string="Closure")
    drainage = fields.Many2one('indimedi.ipd.opnote.drainage',ondelete="cascade", string="Drainage")
    histopathology = fields.Many2one('indimedi.ipd.opnote.histopathology',ondelete="cascade", string="Specimen")
    comments = fields.Many2one('indimedi.ipd.opnote.comments',ondelete="cascade", string="Comments")
    complications = fields.Text(string="Complications")
    procedure = fields.Text(string="Procedure")
    procedure_temp_selection = fields.Many2one('procedure.template.selection',string='Operative Steps')
    procedure_template = fields.Html(related='procedure_temp_selection.template',string='Procedure Template')
    op_morbidity_ids = fields.One2many('op.operative.morbidity','op_operative_morbidity_id', string="Morbidity")
    #anaesthesia
    hbsag_ve_p = fields.Boolean(string="+ve")
    hbsag_ve_m = fields.Boolean(string="-ve")
    hiv_ve_p = fields.Boolean(string="+ve")
    hiv_ve_m = fields.Boolean(string="-ve")
    procedure_name = fields.Char(string="Name of Procedure")
    procedure_date = fields.Datetime(string="Date of Procedure")
    nyha_1 = fields.Boolean('1')
    nyha_2 = fields.Boolean('2')
    nyha_3 = fields.Boolean('3')
    nyha_4 = fields.Boolean('4')
    past_hist_hosp_ids = fields.One2many('past.history.hospitalization','past_history_hosp_id',string="Past History of Hospitalization")
    past_hist_op_ids = fields.One2many('past.history.operation','past_history_op_id',string="Past History of Operation")
    general_look = fields.Selection([('good','Good'),('fair','Fair'),('poor','Poor'),('toxic','Toxic')],string='General Look')
    tongue = fields.Selection([('pink','Pink'),('pale','Pale'),('coated','Coated'),('cyanosed','Cyanosed')],string='Tongue')
    nail = fields.Selection([('pink','Pink'),('pale','Pale'),('clubbing','clubbing')],string='Nail')
    dentition = fields.Selection([('normal','Normal'),('loose','Loose'),('denture','Denture')],string='Dentition')
    temperature = fields.Selection([('normal','Normal'),('raised','Raised')],string='Temperature')
    pupils = fields.Selection([('lens','Lens'),('yes','Yes')],string='pupils')
    sclera = fields.Selection([('white','White'),('blue','Blue'),('yellow','Yellow'),('no','No')],string='Sclera')
    obesity = fields.Selection([('present','Present'),('absent','Absent')],string='Obesity')
    oedema_feed = fields.Selection([('normal','Normal'),('present','Present')],string='Oedema Feed')
    spine = fields.Selection([('normal','Normal'),('deformed','Deformed')],string='Spine')
    ane_personal_history_ids = fields.One2many('anesthesia.personal.history','anesthesia_personal_history_id', string='Personal History')
    se_cvs = fields.Char(string='CVS')
    se_pulse = fields.Char(string='Pulse')
    se_bp = fields.Char(string='BP')
    se_s1s2 = fields.Char(string='S1,S2')
    se_auscultation = fields.Char(string='Auscultation')
    se_cns = fields.Char(string='CNS')
    se_gcs = fields.Char(string='GCS')
    se_gi = fields.Char(string='GI')
    se_liver = fields.Char(string='Liver')
    se_spieen = fields.Char(string='Spleen')
    se_ascites = fields.Char(string='Ascites')
    se_mpc = fields.Char(string='MPC grading')
    se_rs = fields.Char(string='RS')
    se_air_entry = fields.Char(string='Air entry')
    se_foreign_sounds = fields.Char(string='Foreign Sounds')
    se_ronchi = fields.Char(string='Ronchi')
    se_crepts = fields.Char(string='Crepts')
    se_spo2 = fields.Char(string='Spo2 on air')
    se_bht = fields.Char(string='BHT')
    pre_operative_instructions_ids = fields.One2many('anesthesia.pre.operative.instructions','anesthesia_pre_operative_instructions_id',string="Pre-operative Instructions")
    bg_hb = fields.Char(string="HB")
    bg_pc = fields.Char(string="PC")
    bg_tc = fields.Char(string="TC")
    bg_pt = fields.Char(string="PT")
    bg_aptt = fields.Char(string="APTT")
    bg_s_billirubin = fields.Char(string="S.Billirubin")
    bg_sgpt = fields.Char(string="SGPT")
    bg_sgot = fields.Char(string="SGOT")
    bg_alkaline = fields.Char(string="Alkaline")
    bg_s_aluminum = fields.Char(string="S.Aluminum")
    bg_amylase = fields.Char(string="Amylase")
    bg_lipase = fields.Char(string="Lipase")
    bg_s_creatinine = fields.Char(string="S.Creatinine")
    bg_bl_urea = fields.Char(string="Bl. Urea")
    bg_bl_sugar = fields.Char(string="Bl Sugar")
    bg_na_plus = fields.Char(string="Na++")
    bg_k_plus = fields.Char(string="K++")
    bg_cl_minus = fields.Char(string="Cl-")
    bg_ecg = fields.Char(string="ECG")
    bg_cx_ptf = fields.Char(string="Cx R(PA)/PFT")
    bg_blood_gas = fields.Char(string="Blood gas")
    bg_ctscan = fields.Char(string="CT Scan")
    bg_mri = fields.Char(string="MRI")
    bg_sd_echo = fields.Text('2D Echo')
    bg_ph = fields.Char(string="PH")
    bg_pco2 = fields.Char(string="PCo2")
    bg_po2 = fields.Char(string="Po2")
    bg_hco = fields.Char(string="HCo")
    bg_be = fields.Char(string="Be")
    bg_spo2 = fields.Char(string="Spo2")
    bg_tco2 = fields.Char(string="TCO2")
    other_investigations_ids = fields.One2many('other.investigations','other_investigations_id','Other Investigations')
    risk_1 = fields.Boolean(string='1')
    risk_2 = fields.Boolean(string='2')
    risk_3 = fields.Boolean(string='3')
    risk_4 = fields.Boolean(string='4')
    risk_5 = fields.Boolean(string='5')
    risk_e = fields.Boolean(string='E')
    #Anasthesia Major
    major_datetime = fields.Datetime(string="Date & Time")
    inform_consent = fields.Boolean(string="Informed Consent")
    high_risk_consent = fields.Boolean(string="High Risk Consent")
    major_blood_group = fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')], string='Blood Group')
    pre_op_vitals = fields.Char(string="Pre-op Vitals")
    consciousness = fields.Char(string="Consciousness")
    major_temp = fields.Integer(string="Temp")
    major_pulse = fields.Integer(string="Pulse")
    major_bp = fields.Integer(string="BP")
    major_bp2 = fields.Integer(string="")
    major_spo2 = fields.Integer(string="Spo2")
    major_rr = fields.Integer(string="RR")
    urine_output = fields.Integer(string="Urine Output")
    major_diagnosis_id = fields.Many2one('hms.diseases',string='Diagnosis')
    major_procedure = fields.Char(string="Procedure")
    major_surgeon_id = fields.Many2one('hms.physician', string="Surgeon")
    major_anaesthesiologist = fields.Many2one('hms.physician', string="Anaesthesiologist")
    nbm_status = fields.Char(string="NBM Status")
    asa_grade = fields.Char(string="ASA Grade")
    anaesthesia_type = fields.Char(string="Type of Anaesthesia")
    general_type = fields.Boolean(string="General")
    spinal_type = fields.Boolean(string="Spinal")
    regional_type = fields.Boolean(string="Regional")
    preop_procedure = fields.Char(string="Preoperative Procedures")
    #Premeditation
    glyco = fields.Integer(string="Glyco (mg)")
    fentanyl = fields.Integer(string="Fentanyl (mg)")
    rantac_pantodac = fields.Integer(string="Rantac/Pantodac (mg)")
    midaz = fields.Integer(string="Midaz (mg)")
    emset = fields.Integer(string="Emset (mg)")
    diclofenac = fields.Integer(string="Diclofenac (mg)")
    xylocard = fields.Integer(string="Xylocard (mg)")
    paracetamol = fields.Integer(string="Paracetamol (mg)")
    dex_rate1 = fields.Float(string="")
    dex_rate2 = fields.Float(string="")
    major_antibiotic = fields.Char(string="Antibiotics")
    major_iv_propofol = fields.Integer(string="Propofol (mg)")
    major_iv_pentothal = fields.Integer(string="Pentothal (mg)")
    major_iv_ketamine = fields.Integer(string="Ketamine (mg)")
    major_iv_etomidate = fields.Integer(string="Etomidate (mg)")
    # iv_induction = fields.Selection([('propofol','Propofol (mg)'),('pentothal','Pentothal (mg)'),('ketamine','Ketamine (mg)'),('etomidate','Etomidate (mg)')],string="IV Induction")
    # iv_value = fields.Char(string="")
    # muscle_relaxant = fields.Selection([('atarcurium','Atarcurium (mg)'),('rocuronium','Rocuronium (mg)'),('vecuronium','Vecuronium (mg)')],string="Muscle Relaxant")
    # muscle_relaxant_val = fields.Char(string="")
    major_mr_succinyl = fields.Integer(string="Succinyl Choline (mg)")
    major_mr_atarcurium = fields.Integer(string="Atarcurium (mg)")
    major_mr_rocuronium = fields.Integer(string="Rocuronium (mg)")
    major_mr_vecuronium = fields.Integer(string="Vecuronium (mg)")
    iv_line_ra = fields.Many2one('ivline.ra', string="IV Line RA")
    iv_line_la = fields.Many2one('ivline.la', string="IV Line LA")
    ryle_tube = fields.Selection([('12','12'),('14','14'),('16','16'),('18','18'),('20','20')])
    folye = fields.Char(string="Folye's")
    g_major = fields.Char(string="G")
    cvp = fields.Selection([('right_ijv','Right IJV'),('right_subclavian','Right Subclavian'),('right_femoral','Right Femoral'),
                            ('left_ijv','Left IJV'),('left_subclavian','Left Subclavian'),('left_femoral','Left Femoral')],string="CVP")
    warmer = fields.Boolean(string="Warmer")
    dvt_pump = fields.Boolean(string="DVT Pump")
    arterial_line = fields.Char(string="Arterial Line")
    ###intubation
    blade_no = fields.Char(string="Laryngoscope Blade No.")
    endo_tube = fields.Selection([('cuffed','Cuffed'),('uncuffed','Uncuffed')] ,string="Endotracheal Tube")
    endo_tube_val = fields.Char(string="")
    easy_difficult = fields.Selection([('bougle_guided','Bougle guided'),('stylet','Stylet'),('trupti_blade','Trupti Blade'),('burp','Burp'),('fiberoptic','Fiberoptic')], string="Easy / Difficult")
    lma = fields.Char(string="LMA")
    i_gel = fields.Char(string="I-GEL")
    tracheostomy = fields.Char(string="Tracheostomy")
    ###Maintainance of GA
    o2_major = fields.Char(string="O2 (%)")
    n2o_air = fields.Char(string="N2O/Air (%)")
    ippv = fields.Char(string="IPPV (%)")
    vol_control = fields.Boolean(string="Volume Control")
    pressure_control = fields.Boolean(string="Pressure Control")
    isoflurane = fields.Boolean(string="Isoflurane")
    sevoflurane = fields.Boolean(string="Sevoflurane")
    rr_major = fields.Char(string="RR")
    peep = fields.Char(string="PEEP")
    atracurium_rocuronium = fields.Char(string="+ Atracurium / Rocuronium")
    tidal_vol = fields.Char(string="Tidal Volume")
    fio2 = fields.Char(string="FiO2")
    ###Breathing Circuit
    breath_circuit = fields.Selection([('bain','Bain'),('circle_absorder','Circle Absorder'),('spontaneous','Spontaneous'),('jackson','Jackson Rees Circuit')], string="Breathing Circuit")
    glyco_major = fields.Char(string="Glyco")
    neostigmine = fields.Char(string="Neostigmine")
    extubation = fields.Boolean(string="Extubation")
    ###Intrs Operative Vital
    intra_op_vital_ids = fields.One2many('intra.op.vital','inpatient_id', string="Intra Operative Vital Parameters")
    ###Spinal/Epidural
    position_major = fields.Char(string="Position")
    level_major = fields.Char(string="Level")
    needle_major = fields.Selection([('23g','23 G'),('25g','25 G'),('27g','27 G')], string="Needle")
    adjuvant = fields.Char(string="Adjuvant")
    effect_level = fields.Char(string="Effect Level")
    position_epidural = fields.Char(string="Position")
    level_epidural = fields.Char(string="Level")
    depth_catheter = fields.Char(string="Depth of Catheter")
    spinal_drug_ids = fields.One2many('spinal.drug','inpatient_id', string="Spinal/Epidural Anaesthesia Medication")
    ###Post Operative Vital Parameter
    time_po = fields.Datetime(string="Time")
    urine_po = fields.Integer(string="Urine Output")
    consciousness_po = fields.Char(string="Consciousness")
    blood_loss_po = fields.Integer(string="Blood Loss")
    puls_po = fields.Integer(string="Pulse")
    crystalloids = fields.Char(string="Crystalloids")
    bp_po = fields.Integer(string="BP")
    bp_po2 = fields.Integer(string="")
    colloids = fields.Char(string="Colloids")
    spo2_po = fields.Integer(string="SPO2")
    blood_prod_po = fields.Char(string="Blood Products")
    muscle_tone = fields.Char(string="Muscle Tone")
    oxygen_supple = fields.Char(string="Oxygen Supplement")
    pain_po = fields.Char(string="Pain")
    post_op_inv = fields.Char(string="Post Op Investigations")
    ###Post Of Advice
    # nbm_advice = fields.Char(string="NBM (Hours)")
    # head_low = fields.Boolean(string="Head Low")
    # chest_position = fields.Boolean(string="Chest Position 30º Head up")
    # iv_fluids_advice = fields.Char(string="IV Fluids (ml/hour)")
    # watch_for_vital = fields.Boolean(string="Watch for Vitals")
    # shift_icu = fields.Boolean(string="Shift to ICU")
    # recovery_room = fields.Char(string="Recovery Room")
    post_advice_ids = fields.One2many('post.ans.advice','inpatient_id', string="Post Of Advice")
    ###Post Operative Pain Management
    diclofenac = fields.Char(string="Diclofenac")
    tramadol = fields.Char(string="Tramadol")
    others_po = fields.Char(string="Others")
    tramadol_inj = fields.Char(string="Inj. Tramadol (ml)")
    emset_inj_to = fields.Char(string="Inj. Emset ")
    ml_from = fields.Char(string="ml")
    ns_trama = fields.Char(string="ml in 0.9% NS @")
    inj_fentanyl = fields.Char(string="Inj. Fentanyl")
    ns_from = fields.Char(string="ml + 0.9% NS")
    ns_to = fields.Char(string="ml @")
    inj_midazolam = fields.Char(string="Inj. Midazolam")
    minda_fentanyl = fields.Char(string="ml + Inj. Fentanyl")
    minda_ns_from = fields.Char(string="ml + 0.9% NS")
    minda_ns_to = fields.Char(string="ml @")
    inj_atracurium = fields.Char(string="Inj. Atracurium")
    atra_ns = fields.Char(string="ml + 0.9% NS @")
    inj_ropi = fields.Char(string="Inj. Ropivanalne 0.2%")
    ropi_fentnyl = fields.Char(string="ml + Inj. Fentanyl")
    ropi_ns = fields.Char(string="ml in 0.96% NS @")
    inj_trama = fields.Char(string="Inj. Tramadol")
    trama_ns = fields.Char(string="ml in 0.9% NS @")
    rectal_sup = fields.Text(string="Rectal Suppositories")
    post_major_anaes = fields.Many2one('res.users', string="Name of Anaesthetist", default=lambda self: self.env.user, readonly="True")
    #Minor Anaesthesia Form
    anaesthesia_plan = fields.Selection([('ga','GA'),('regional','Regional')], string="Anaesthesia Plan")
    proc_name = fields.Char(string="Procedure Name")
    asa_risk_1 = fields.Boolean(string='1')
    asa_risk_2 = fields.Boolean(string='2')
    asa_risk_3 = fields.Boolean(string='3')
    asa_risk_r = fields.Boolean(string='R')
    asa_risk_e = fields.Boolean(string='E')
    pre_illness = fields.Char(string="Pre Existing Illness")
    minor_medication = fields.Char(string="Medication")
    minor_investigation = fields.Char(string="Investigations")
    minor_note = fields.Char(string="Anaesthesia Note")
    minor_fentanyl = fields.Char(string="Inj Fentanyl (mcg i.v.)")
    minor_midaz = fields.Char(string="Inj Midaz (mg i.v.)")
    minor_emeset = fields.Char(string="Inj Emeset (mg i.v.)")
    minor_pantoprazole = fields.Char(string="Inj Pantoprazole (mg i.v.)")
    minor_glyco = fields.Char(string="Glyco")
    minor_rantac = fields.Char(string="Rantac")
    minor_xylocard = fields.Char(string="Xylocard")
    minor_attending = fields.Many2one('hms.physician', string="Attending Doctor")
    minor_consulting = fields.Many2one('hms.physician', string="Consulting Doctor")
    minor_antibiotic = fields.Char(string="Antibiotics")
    minor_induction = fields.Selection([('iv_induction','I.V Induction Drug'),('scoline','Scoline'),('muscle_relax','Muscle Relaxant')] ,string="Induction")
    minor_induction_val = fields.Char(string="Induction Value")
    minor_position = fields.Selection([('supine','Supine Lithotomy'),('prone','Prone Jack Knife')], string="Poistion")
    minor_endo_tube = fields.Selection([('7','7'),('8','8')], string="Endotracheal Tube No.")
    minor_endo_tube_val = fields.Char(string="Endotracheal Tube Value")
    minor_gel = fields.Selection([('3','3'),('4','4'),('5','5')], string="I Gel No.")
    minor_gel_val = fields.Char(string="I Gel Value")
    minor_o2 = fields.Char(string="O2")
    minor_n2o_air = fields.Char(string="N2O/Air")
    minor_ippv = fields.Char(string="IPPV")
    minor_iso_sevo = fields.Char(string="Isoflurane/Sevoflurane")
    minor_atracurium = fields.Char(string="Atracurium")
    minor_advice_nbm = fields.Char(string="NBM till further order")
    minor_advice_head = fields.Boolean(string="Head low position")
    minor_advice_hydration = fields.Boolean(string="Maintain Hydration")
    minor_advice_vital = fields.Boolean(string="Watch for vitals")
    minor_advice_conscious = fields.Boolean(string="Consciousness")
    minor_advice_pain = fields.Boolean(string="Pain score")
    minor_advice_inform = fields.Char(string="Inform sos")
    post_minor_anaes = fields.Many2one('res.users', string="Name of Anaesthetist", default=lambda self: self.env.user, readonly="True")
    #post-op-orders
    stage_post = fields.Selection([('elective','Elective'),('emergency','Emergency'),('non_emergency','Non Emergency Urgent')])
    start_time_post = fields.Datetime(string="Start Time")
    comp_time_post = fields.Datetime(string="Completion Time")
    lap_post = fields.Selection([('lap','Lap'),('lap_assisted','Lap Assisted'),('lap_convert','Lap Converted Open'),('lap_open','Open')])
    under_post = fields.Selection([('ga','GA'),('short_ga','Short GA'),('epi_ga','Epi+GA'),('sa','SA')])
    nbm_post = fields.Char(string="NBM")
    do_monitor_post = fields.Char(string="D/O Monitoring")
    vitals_monitor_post = fields.Char(string="Vitals Monitoring")
    ag_monitor_post = fields.Char(string="AG Monitoring")
    io_monitor_post = fields.Char(string="I/O Monitoring")
    io_uop_post = fields.Char(string="Intra-op UOP (ml)")
    io_pcv_post = fields.Char(string="Intra-op PCV (units)")
    io_blood_loss_post = fields.Char(string="Intra-op Blood Loss (ml)")
    ffp_post = fields.Char(string="FFP (units)")
    duration_post = fields.Char(string="Duration (min)")
    crystalloids_post = fields.Char(string="Crystalloids (ml)")
    specimen_post = fields.Char(string="Specimen")
    plus_post = fields.Boolean(string="Plus")
    bile_post = fields.Boolean(string="Bile")
    ascitic_post = fields.Boolean(string="Ascitic Fluid")
    rm_post = fields.Boolean(string="R/M")
    cs_post = fields.Boolean(string="C/S")
    cytology_post = fields.Boolean(string="Cytology")
    amylase_post = fields.Boolean(string="Amylase")
    ada_post = fields.Boolean(string="ADA")
    hpe_post = fields.Boolean(string="HPE")
    fnac_post = fields.Boolean(string="FNAC")

    #assessement
    fellow_ids = fields.One2many('inpatient.checklist.fellow', 'surgery_id', string='Fellow', default=lambda self: self._default_fellow())
    anesthetist_ids = fields.One2many('inpatient.checklist.anesthetist', 'surgery_id', string='Anesthetist', default=lambda self: self._default_anesthetist())
    operating_surgeon_ids = fields.One2many('inpatient.checklist.operating.surgeon', 'surgery_id', string='Operating Surgeon', default=lambda self: self._default_operating_surgeon())
    scrub_nurse_ids = fields.One2many('inpatient.checklist.scrub.nurse', 'surgery_id', string='Scrub Nurse', default=lambda self: self._default_scrub_nurse())
    otincharge_ids = fields.One2many('inpatient.checklist.otincharge', 'surgery_id', string='OT in charge', default=lambda self: self._default_otincharge())
    recovery_nurse_ids = fields.One2many('inpatient.checklist.recovery.checklist', 'surgery_id', string='Recovery Nurse', default=lambda self: self._default_recovery())


    #Nurse:---Pre Operative Checklist
    pre_op_datetime = fields.Datetime(string="Date & Time of Surgery")
    surgeon_id = fields.Many2one('hms.physician', string="Surgeon")
    anesthetist_id = fields.Many2one('hms.physician', string="Anesthetist")
    high_risk = fields.Boolean(string="High Risk")
    hiv_positive = fields.Boolean(string="HIV Positive")
    hbsag_preop = fields.Boolean(string="HBsAg")
    allergy_preop = fields.Char(string="Allergy")
    pulse_preop = fields.Float(string="Pulse")
    temp_preop = fields.Float(string="Temp")
    rr_preop  = fields.Float(string="RR")
    bp_preop = fields.Float(string="BP")
    spo2_preop = fields.Float(string="Spo2")
    rbs_preop = fields.Float(string="RBS")
    hb_preop = fields.Float(string="HB")
    blood_group_preop = fields.Selection([('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')], string='Blood Group')
    investigation_preop_ids = fields.One2many('preoperative.investigation','nurse_hms_id', string="Investigation", default=lambda self: self._default_preopinvchecklist())
    information_preop_ids = fields.One2many('preoperative.information','nurse_hms_id', string="Information", default=lambda self: self._default_preopinfochecklist())
    ward_nurse_id = fields.Many2one('res.users', ondelete="cascade", string='Ward Nurse', domain=[('is_nurse','=',True)])
    preop_nurse_id = fields.Many2one('res.users', ondelete="cascade", string='Pre-Op Nurse',domain=[('is_nurse','=',True)])
    ot_nurse_id = fields.Many2one('res.users', ondelete="cascade", string='OT Nurse', domain=[('is_nurse','=',True)])
    medicaments_grps_ids = fields.Many2one('medicaments.grps',string='Medicaments Groups')
    

    @api.onchange('medicaments_grps_ids')
    def onchange_medicaments_grps_ids(self):
            product_lines = []
            for rec in self:
                for line in rec.medicaments_grps_ids.mapped('medicaments_line'):
                    product_lines.append((0,0,{
                        'product_id': line.product_id.id,
                    }))
                rec.medicament_line = product_lines

    @api.model
    def create(self, values):
        print "=============",self.duration
        res = super(SurgeryReg, self).create(values)
        if values.get('name', 'Surgery #') == 'Surgery #':
            res.name = self.env['ir.sequence'].next_by_code('inpatient.registration.surgery') or 'Hospitalization #'
        return res
        
    @api.multi
    def _time_count(self):
        for task in self:
            if task.start_date:
                ends = datetime.strptime(task.end_date, '%Y-%m-%d %H:%M:%S')
                start = datetime.strptime(task.start_date, '%Y-%m-%d %H:%M:%S')
                datetime_diff = datetime.strptime(task.end_date, '%Y-%m-%d %H:%M:%S') - datetime.strptime(task.start_date, '%Y-%m-%d %H:%M:%S')
                m, s = divmod(datetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (('%0*d')%(2,h))
                dur_m = (('%0*d')%(2,m*1.677966102))
                duration = dur_h+'.'+dur_m
                task.duration = float(duration) * 60
            elif task.end_date :
                task.duration = 0.0

    @api.multi
    def action_confirm(self):
        self.state = 'confirm'

    @api.multi
    def action_inprogress(self):
        if self.state == 'confirm':
            self.bed_id.write({'state': 'occupied'})
            history_obj = self.env['patient.accomodation.history']
            history_obj.create({
                'inpatient_id': self.inpatient_id.id,
                'surgery_id': self.id,
                'patient_id': self.inpatient_id.patient_id.id,
                'ward_id':self.ward_id.id,
                'bed_id':self.bed_id.id,
                'start_date':datetime.now(),
                'department_id': self.department_id.id,
                'type': 'surgery',
            })
            self.state = 'progress'

    @api.multi
    def action_done(self):
        accomodation_history_obj = self.env['patient.accomodation.history']
        if self.state == 'progress':
            self.bed_id.write({'state': 'free'})
            hist_id = accomodation_history_obj.search([('surgery_id','=', self.id), ('bed_id', '=', self.bed_id.id)])
            if hist_id:
                accomodation_history_obj.browse([max(hist_id.ids)]).write({'end_date': datetime.now()})
            self.state = 'done'


#Fellow
class POCFellow(models.Model):
    _name = 'inpatient.checklist.fellow'

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one("inpatient.registration.surgery", ondelete="cascade", string="Hospitalization")

class POCFellowTemplate(models.Model):
    _name="inpatient.checklist.fellow.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")

#Anesthetist
class POCAnesthetist(models.Model):
    _name = 'inpatient.checklist.anesthetist'

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one("inpatient.registration.surgery", ondelete="cascade", string="Hospitalization")

class POCAnesthetistTemplate(models.Model):
    _name="inpatient.checklist.anesthetist.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")

#OperatingSurgeon
class POCOperatingSurgeon(models.Model):
    _name = 'inpatient.checklist.operating.surgeon'

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one("inpatient.registration.surgery", ondelete="cascade", string="Hospitalization")

class POCOperatingSurgeonTemplate(models.Model):
    _name="inpatient.checklist.operating.surgeon.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")

#ScrubNurse
class ScrubNurse(models.Model):
    _name = 'inpatient.checklist.scrub.nurse'

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one("inpatient.registration.surgery", ondelete="cascade", string="Hospitalization")

class ScrubNurseTemplate(models.Model):
    _name="inpatient.checklist.scrub.nurse.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")

#OTinCharge
class OTinCharge(models.Model):
    _name = "inpatient.checklist.otincharge"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one("inpatient.registration.surgery", ondelete="cascade", string="Hospitalization")

class OTinChargeTemplate(models.Model):
    _name="inpatient.checklist.otincharge.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")

#Recovery Checklist
class RecoveryChecklist(models.Model):
    _name = "inpatient.checklist.recovery.checklist"

    name = fields.Char(string="Name")
    is_done = fields.Boolean(string="Y/N", default=False)
    remark = fields.Char(string="Remarks")
    surgery_id = fields.Many2one("inpatient.registration.surgery", ondelete="cascade", string="Hospitalization")

class RecoveryChecklistTemplate(models.Model):
    _name="inpatient.checklist.recovery.checklist.template"

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remarks")

class PreoperativeInvestigation(models.Model):
    _name = 'preoperative.investigation'

    nurse_hms_id = fields.Many2one('inpatient.registration.surgery', string="Hospitalization")
    name = fields.Char(string="Investigation", readonly="1")
    preop_done = fields.Boolean(string="Yes / No")
    copy_no = fields.Integer(string="No of copies")

class PreoperativeInformation(models.Model):
    _name = 'preoperative.information'

    nurse_hms_id = fields.Many2one('inpatient.registration.surgery', string="Hospitalization")
    name = fields.Char(string="Content", readonly="1")
    info_done = fields.Boolean(string="Yes / No")

class ProcedureTemplateSelection(models.Model):
    _name = 'procedure.template.selection'

    name = fields.Char(string='Name')
    template = fields.Html(string='Template')


class MedicamentsGroupLine(models.Model):
    _name = 'medicaments.group.line'

    product_id = fields.Many2one('product.product', ondelete="cascade", string='Consumable')
    medicaments_group_id = fields.Many2one('medicaments.grps',string='Medicaments')

class MedicamentsGrps(models.Model):
    _name = 'medicaments.grps'

    name = fields.Char(string='Medicine Name')
    medicaments_line = fields.One2many('medicaments.group.line', 'medicaments_group_id', 'Line')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: