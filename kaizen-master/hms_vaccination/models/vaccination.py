#-*- coding: utf-8 -*-
from openerp import api, fields, models
from datetime import date, datetime, timedelta as td

class VaccinationGroupLine(models.Model):
    _name = 'vaccination.group.line'

    group_id = fields.Many2one('vaccination.group', 'Group')
    product_id = fields.Many2one('product.product', 'Product', domain=[('hospital_product_type', '=', "vaccination")])


class VaccinationGroup(models.Model):
    _name = 'vaccination.group'

    name = fields.Char(string='Group Name', required=True)
    group_line = fields.One2many('vaccination.group.line', 'group_id', string='Medicament line')


class IndimediProduct(models.Model):
    _inherit = 'product.template'

    hospital_product_type = fields.Selection(selection_add=[('vaccination','Vaccination'),('prescription','Prescription')])
    date_due_day = fields.Integer('Due Days',help="How many days before message to be triggered")


class IndimediPatient(models.Model):
    _inherit = 'hms.patient'
    
    vaccination_group_id = fields.Many2one('vaccination.group',string='Vaccination Group')
    vaccination_line = fields.One2many('vaccination.vaccination','patient_id', 'Vaccination')

    # @api.onchange('vaccination_group_id')
    # def onchange_vaccination_group_id(self):
    #     product_lines = []
    #     if self.dob:
    #         dob = fields.Date.from_string(self.dob)
    #         for line in self.vaccination_group_id.group_line:
    #             days = line.product_id.date_due_day
    #             product_lines.append((0,0,{
    #                 'product_id': line.product_id.id, 
    #                 'date_check_due': (dob+ td(days=days))
    #             }))
    #     else:
    #         for line in self.vaccination_group_id.group_line:
    #             product_lines.append((0,0,{
    #                 'product_id': line.product_id.id,
    #             }))
    #     self.vaccination_line = product_lines


class Vaccination(models.Model):
    _name = 'vaccination.vaccination'

    patient_id = fields.Many2one('hms.patient','Patient', help="Patient for vaccination")
    product_id = fields.Many2one('product.product', 'Vaccination', domain=[('hospital_product_type', '=', "vaccination")])
    date_check_due = fields.Date('Due Date')
    check = fields.Boolean('Check', default=False)
    given_date = fields.Date('Given Date')
    batch = fields.Binary('Batch Photo')

    @api.onchange('check')
    def onchange_check(self):
        if self.check:
            for rec in self:
                rec.given_date = fields.Date.today()
                
    @api.onchange('product_id')
    def onchange_vaccination_type(self):
        if self.product_id and self.patient_id.dob:
            for rec in self:
                dob = fields.Date.from_string(rec.patient_id.dob)
                days = rec.product_id.date_due_day
                rec.date_check_due = (dob+ td(days=days))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
