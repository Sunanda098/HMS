# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime
import os, base64, imghdr

from openerp.tools import config

class Investigation(models.Model):
    _inherit = 'hms.investigation'

    @api.model
    def create(self, values):
        res = super(Investigation, self).create(values)
        res.load_image_from_folder()
        return res

    @api.multi
    def load_image_from_folder(self):
        if self.investigation_type != 'radiology':
            return self.fetch_images()
           
        patient_path = self.patient_id.name.replace(' ', '_')+'-'+self.name
        date_inv = self.date_investigation.split(' ')[0]
        radiology_path = os.path.join("Radiology", self.env.cr.dbname, date_inv, patient_path)
        db_path = os.path.join('/media')
        path = os.path.join(db_path, radiology_path)
        if not os.path.isdir(path):
            os.makedirs(path, 0777)
        doc_obj = self.env['document.management']
        for resource in os.listdir(path):
            if imghdr.what(os.path.join(path, resource)) in ('png', 'jpg', 'jpeg','gif', 'xcf'):
                file_name = resource.replace('.', '-')
                os.rename(os.path.join(path, resource), os.path.join(path, file_name))
                radiology_file_path = os.path.join(radiology_path, file_name)
                ir_att_id = doc_obj.search([
                    ('name', '=', file_name),
                    ('investigation_id', 'in', self.ids)])
                if not ir_att_id:
                    binary = base64.encodestring(open(os.path.join(path, file_name)).read())
                    values = {
                        'is_document': binary,
                        'patient_id': self.patient_id.id,
                        'name': file_name,
                        'investigation_id': self.id,
                    }
                    doc_id = doc_obj.create(values)

    @api.multi
    def write(self, values):
        res = super(Investigation, self).write(values)
        self.load_image_from_folder()
        return res
#13467