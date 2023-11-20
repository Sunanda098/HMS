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

class IndimediDiseaseGene(models.Model):

    _name = 'disease.gene'
    _description = 'Disease Genes'

    name = fields.Char(string='Official Symbol', size=256, required=True)
    gene_id = fields.Char(string='Gene ID', size=256)
    long_name = fields.Char(string='Official Long Name', size=256, required=True)
    location = fields.Char(string='Location', size=256, required=True, help="Locus of the chromosome")
    chromosome = fields.Char(string='Affected Chromosome', size=256, required=True)
    info = fields.Text(string='Information')
    dominance = fields.Selection([('d', 'dominant'),('r', 'recessive')], 'Dominance', select=True)    

IndimediDiseaseGene()


class PatientGeneticRisk(models.Model):
    
    _name = 'hms.patient.genetic.risk'
    _description = 'Patient Genetic Risks'
    
    patient_id = fields.Many2one('hms.patient', ondelete='restrict', string='Patient', select=True)
    disease_gene = fields.Many2one('disease.gene', ondelete='restrict',string='Disease Gene', required=True)

PatientGeneticRisk()

class FamilyDiseases(models.Model):
    
    _name = 'hms.patient.family.diseases'
    _description = 'Family Diseases'

    patient_id = fields.Many2one('hms.patient', ondelete='restrict', string='Patient', select=True)
    name_id = fields.Many2many('hms.diseases', 'rz_id','pz_id','cz_id' ,'Disease', required=True)
    xory = fields.Selection([('m', 'Maternal'),('f', 'Paternal')], 'Maternal or Paternal', select=True)
    relative = fields.Selection([
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('brother', 'Brother'),
    ('sister', 'Sister'),
    ('aunt', 'Aunt'),
    ('uncle', 'Uncle'),
    ('nephew', 'Nephew'),
    ('niece', 'Niece'),
    ('grandfather', 'Grandfather'),
    ('grandmother', 'Grandmother'),
    ('cousin', 'Cousin')], 'Relative',
    help="First degree = siblings, mother and father; second degree = "
    "Uncles, nephews and Nieces; third degree = Grandparents and cousins",required=True)
            
FamilyDiseases()

# class IndimediPatient(models.Model):
#     'Add to the Medical patient_data class (hms.patient) the genetic ' \
#     'and family risks'
#     _inherit='hms.patient'

#     genetic_risks = fields.One2many('hms.patient.genetic.risk', 'patient_id', 'Genetic Risks')
#     family_history = fields.One2many('hms.patient.family.diseases', 'patient_id', 'Family History')

# IndimediPatient()
