# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.techreceptives.com>)
#    Special Credit and Thanks to Thymbra Latinoamericana S.A.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################

from openerp import api, fields, models
from openerp.tools.translate import _


class Content(models.Model):
    _name = 'medicament.content'
    name = fields.Char('Name')
    _sql_constraints = [
        ('name_indimedi_medi_content_uniq', 'unique (name)', 'The name of the Content must be unique !'),
    ]


class Flavour(models.Model):
    _name = 'medicament.flavour'
    name = fields.Char('Name')
    _sql_constraints = [
        ('name_indimedi_medi_flavour_uniq', 'unique (name)', 'The name of the Content must be unique !'),
    ]


class IndimediDiseases(models.Model):
    _name = 'hms.diseases'

    category = fields.Many2one('indiemdi.diseases.category', string='Category', ondelete='cascade',
    help='Select the category for this disease This is usually'\
    'associated to the standard. For instance, the chapter on the ICD-10'\
    'will be the main category for de disease')
    info = fields.Text(string='Extra Info')
    code = fields.Char(size=256, string='Code', help='Specific Code for the Disease (eg, ICD-10)')
    name = fields.Char(size=256, string='Name', required=True, translate=True, help='Disease name')
    protein = fields.Char(size=256, string='Protein involved', help='Name of the protein(s) affected')
    gene = fields.Char(size=256, string='Gene')
    chromosome = fields.Char(size=256, string='Affected Chromosome', help='chromosome number')
    active = fields.Boolean('Active',default=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.code:
                name = record.code + ' - ' + name
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|',('name',operator,name),('code', operator, name)] + args, limit=limit)
        return recs.name_get()

class IndiemdiDiseasesCategory(models.Model):
    _name = 'indiemdi.diseases.category'

    name = fields.Char(size=256, string='Category Name', required=True)
    parent_id = fields.Many2one('indiemdi.diseases.category', ondelete='cascade', string='Parent Category', select=True)

    _constraints = [(models.Model._check_recursion, 'Error ! You cannot create recursive \n' 'Category.', ['parent_id'])]


class IndimediPatientDisease(models.Model):
    _name = 'hms.patient.disease'


    disease = fields.Many2one('hms.diseases', ondelete='set null', string='Disease')
    treatment_description = fields.Char(size=256,string='Treatment Description')
    diagnosed_date = fields.Date(string='Date of Diagnosis')
    healed_date = fields.Date(string='Healed')
    doctor = fields.Many2one('hms.physician', ondelete='restrict', string='Physician',help='Physician who treated or diagnosed the patient')    
    short_comment = fields.Char(size=256, string='Remarks',
    help='Brief, one-line remark of the disease. Longer description will'\
    ' go on the Extra info field')
    is_active = fields.Boolean(string='Active disease')
    is_allergy = fields.Boolean(string='Allergic Disease')
    pregnancy_warning = fields.Boolean(string='Pregnancy warning')
    is_on_treatment = fields.Boolean(string='Currently on Treatment')
    weeks_of_pregnancy = fields.Integer(string='Contracted in pregnancy week #')
    patient_id = fields.Many2one('hms.patient', ondelete='restrict', string='Patient')
    lactation = fields.Boolean('Lactation')
    #EXtra Fields
    disease_severity = fields.Selection([
    ('1_mi', 'Mild'),
    ('2_mo', 'Moderate'),
    ('3_sv', 'Severe'),
    ], string='Severity',select=True, sort=False)
    extra_info = fields.Text(string='Extra Info')
    status = fields.Selection([
    ('a', 'acute'),
    ('c', 'chronic'),
    ('u', 'unchanged'),
    ('h', 'healed'),
    ('i', 'improving'),
    ('w', 'worsening'),
    ], string='Status of the disease',select=True, sort=False)
    date_stop_treatment = fields.Date(string='End',help='End of treatment date')
    is_infectious = fields.Boolean(string='Infectious Disease',
    help='Check if the patient has an infectious' \
    'transmissible disease')
    allergy_type = fields.Selection([
    ('da', 'Drug Allergy'),
    ('fa', 'Food Allergy'),
    ('ma', 'Misc Allergy'),
    ('mc', 'Misc Contraindication'),
    ], string='Allergy type',select=True, sort=False)
    age = fields.Integer(string='Age when diagnosed',help='Patient age at the moment of the diagnosis. Can be estimative')
    date_start_treatment = fields.Date(string='Start',help='Start of treatment date')
