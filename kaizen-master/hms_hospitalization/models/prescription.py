from openerp import api, fields, models
from openerp.tools.translate import _

class inpatient_prescription(models.Model):
    _inherit = ['prescription.order']

    inpatient_registration_code = fields.Many2one('inpatient.registration', ondelete="restrict", string='Hospitalization',help="Enter the patient hospitalization code")
    ward_no= fields.Many2one('hospital.ward',string='Ward/Room No.', ondelete="restrict")
    bed_no = fields.Many2one("hospital.bed",string="Bed No.", ondelete="restrict")

