# -*- encoding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.osv import  osv

class BaseConfigSettings(osv.TransientModel):
    _inherit = 'base.config.settings'
    
    is_sms_user = fields.Boolean('Setup CellApps SMS Getway')
    user_name = fields.Char('User Name')
    password = fields.Char('Password')
    sender_id = fields.Char('Sender Id')
    url = fields.Char('URL')


    def get_default_sms_getway_details(self, cr, uid, fields, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return {'is_sms_user': user.company_id.is_sms_user, 'user_name': user.company_id.user_name, 'password': user.company_id.password, 'sender_id': user.company_id.sender_id, 'url': user.company_id.url}

    def set_sms_getway_details(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        user.company_id.write({'is_sms_user': config.is_sms_user, 'user_name': config.user_name, 'password': config.password, 'sender_id': config.sender_id, 'url': config.url})

    def test_sms(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        if config.is_sms_user:
            format_number = '9033584086'
            if " " in format_number: format_number.replace(" ", "")
            if "+" in format_number: format_number = format_number.replace("+", "")
            url = "http://sms.cellapps.com/sendsms_bulk.php?UserId=" + str(config.user_name) + "&Pwd=" + str(config.password) + "&SenderId=" + str(config.sender_id) + "&Mobileno=" + str(format_number) + "&Msg=" + str('Test')
            response_string = requests.get(url)

            response_code = ""
            if "FAILURE : Sender Invalid" in response_string.text:
                response_code = "BAD CREDENTIALS"
            elif "FAILURE : On URL" in response_string.text:
                response_code = "BAD URL"
            elif "FAILURE : Invalid Password" in response_string.text:
                response_code = "Authentication failed"
            elif "SUCCESS" in response_string.text:
                response_code = "Test Successfully"
            else:
                response_code = response_string.text

            raise osv.except_osv(_('Test Result'), _(response_code))
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
