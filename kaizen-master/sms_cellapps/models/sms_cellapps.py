# -*- coding: utf-8 -*-
import time
import urllib
from openerp import api, fields, models, _
from openerp.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class PartnerSmsSend(models.Model):
    _name = "partner.sms.send"

    @api.one
    def _default_get_mobile(self):
        partner_pool = self.env['res.partner']
        active_ids = self.fields.get('active_ids')
        res = {}
        i = 0
        for partner in partner_pool.browse(active_ids):
            i += 1
            res = partner.mobile
        if i > 1:
            raise UserError(_('You can only select one partner'))
        return res

    mobile_to = fields.Char(string='To', size=256, required=True,default=_default_get_mobile)
    app_id = fields.Char(string='API ID', size=256)
    user = fields.Char(string='Login', size=256)
    password = fields.Char(string='Password', size=256)
    text = fields.Text(string='SMS Message', required=True)
    validity = fields.Integer(string='Validity',
        help='the maximum time -in minute(s)- before the message is dropped')
    classes = fields.Selection([
            ('0', 'Flash'),
            ('1', 'Phone display'),
            ('2', 'SIM'),
            ('3', 'Toolkit')
        ], string='Class', help='the sms class: flash(0), phone display(1), SIM(2), toolkit(3)')
    deferred = fields.Integer(string='Deferred',
        help='the time -in minute(s)- to wait before sending the message')
    priority = fields.Selection([
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3')
        ], 'Priority', help='The priority of the message')
    coding = fields.Selection([
            ('1', '7 bit'),
            ('2', 'Unicode')
        ], string='Coding', help='The SMS coding: 1 for 7 bit or 2 for unicode')
    tag = fields.Char(string='Tag', size=256, help='an optional tag')
    nostop = fields.Boolean(string='NoStop', help='Do not display STOP clause in the message, this requires that this is not an advertising message')

    @api.model
    def _prepare_smscellapps_queue(self,data, name):
        return {
            'name': name,
            'state': 'draft',
            'mobile': data.mobile_to,
            'msg': data.text,
            'validity': data.validity,
            'classes': data.classes,
            'deferred': data.deferred,
            'priority': data.priority,
            'coding': data.coding,
            'tag': data.tag,
            'nostop': data.nostop,
        }

    @api.model
    def _send_message(self, data):
        company = self.env.user.company_id
        if company.is_sms_user:
            url = company.url
            name = url
            prms = {}

            prms['UserId'] = company.user_name
            prms['Pwd'] = company.password
            prms['SenderId'] = company.sender_id
            prms['Mobileno'] = data.mobile_to
            prms['Msg'] = data.text

            params = urllib.urlencode(prms)
            name = url + "?" + params
            queue_obj = self.env['sms.smscellapps.queue']
            vals = self._prepare_smscellapps_queue(data, name)
            queue_obj.create(vals)
        return True

    @api.multi
    def sms_send(self):
        for data in self:
            if not self.env.user.company_id.is_sms_user:
                raise UserError(_('No SMS CellApps configuration Found'))
            else:
                self._send_message(data)
        return {}

    @api.model
    def _check_queue(self):
        queue_obj = self.env['sms.smscellapps.queue']
        history_obj = self.env['sms.smscellapps.history']
        sid_ids = queue_obj.search([('state', '!=', 'send'),('state', '!=', 'sending')], limit=30)
        for sids in sid_ids:
            if sids:
                sids.state = 'sending'
                for sms in sids:
                    
                    try:
                        urllib.urlopen(sms.name)
                    except Exception, e:
                        raise UserError(e)
                    history_obj.create({
                        'name': _('SMS Sent'),
                        'sms': sms.msg,
                        'to': sms.mobile,
                    })
                sids.unlink()


class SMSQueue(models.Model):
    _name = 'sms.smscellapps.queue'
    _description = 'SMS Queue'

    name = fields.Text(string='SMS Request', size=256,required=True, readonly=True,
            states={'draft': [('readonly', False)]},default='SMS Request')
    msg =  fields.Text(string='SMS Text', size=256,required=True, readonly=True,
        states={'draft': [('readonly', False)]})
    mobile =  fields.Char(string='Mobile No', size=256, required=True, readonly=True,
        states={'draft': [('readonly', False)]})
    state =  fields.Selection([
        ('draft', 'Queued'),
        ('sending', 'Waiting'),
        ('sent', 'Sent'),
        ('error', 'Error'),
    ], string='Message Status', select=True, readonly=True,default='draft')
    error =  fields.Text(string='Last Error', size=256,
        readonly=True,
        states={'draft': [('readonly', False)]})
    date_create =  fields.Datetime(string='Date', readonly=True,default=fields.Datetime.now)
    validity =  fields.Integer('Validity',
        help='The maximum time -in minute(s)- before the message is dropped')
    classes =  fields.Selection([
            ('0', 'Flash'),
            ('1', 'Phone display'),
            ('2', 'SIM'),
            ('3', 'Toolkit')
        ], string='Class', help='The sms class: flash(0), phone display(1), SIM(2), toolkit(3)')
    deferred =  fields.Integer(string='Deferred',
        help='The time -in minute(s)- to wait before sending the message')
    priority =  fields.Selection([
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3')
        ], 'Priority', help='The priority of the message ')
    coding =  fields.Selection([
            ('1', '7 bit'),
            ('2', 'Unicode')
        ], string='Coding', help='The sms coding: 1 for 7 bit or 2 for unicode')
    tag =  fields.Char(string='Tag', size=256,
        help='An optional tag')
    nostop =  fields.Boolean(string='NoStop', help='Do not display STOP clause in the message, this requires that this is not an advertising message')

    @api.multi
    def send_sms(self):
        history_obj = self.env['sms.smscellapps.history']
        self.state = 'sending'
        for sms in self:
            try:
                urllib.urlopen(sms.name)
            except Exception, e:
                raise UserError(e)
            history_obj.create({
                'name': _('SMS Sent'),
                'sms': sms.msg,
                'to': sms.mobile,
            })
        self.unlink()


class HistoryLine(models.Model):
    _name = 'sms.smscellapps.history'
    _description = 'SMS Client History'

    name = fields.Char(string='Description', size=160, readonly=True)
    date_create = fields.Datetime(string='Date', readonly=True,default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='Username', readonly=True, select=True)
    to = fields.Char(string='Mobile No', size=15, readonly=True)
    sms = fields.Text(string='SMS', size=160, readonly=True)

    @api.model
    def create(self,vals):
        super(HistoryLine, self).create(vals)
        #self.cr.commit()

class ResCompany(models.Model):
    _inherit = 'res.company'

    is_sms_user = fields.Boolean(string='Setup CellApps SMS Getway',default=True)
    user_name = fields.Char(string='User Name')
    password = fields.Char(string='Password')
    sender_id = fields.Char(string='API')
    url = fields.Char(string='URL',default='http://sms.cellapps.com/sendsms_bulk.php')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: