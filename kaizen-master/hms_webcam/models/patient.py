# -*- encoding: utf-8 -*-

from openerp import api, fields, models, _


class IndimediPatient(models.Model):
    _inherit = 'hms.patient'

    @api.multi
    def action_take_picture(self):
        
        res_id = self.env['ir.model.data'].get_object('hms_webcam', 'action_take_photo')
        dict_act_window = res_id.read()[0]
        if not dict_act_window.get('params', False):
            dict_act_window.update({'params': {}})
        dict_act_window['params'].update({'patient_id': self.ids[0]})
        return dict_act_window

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: