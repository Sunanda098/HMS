# -*- coding: utf-8 -*-

import babel.dates
import time
import datetime
import pytz
from datetime import timedelta
from dateutil import tz

from openerp import http
from openerp import tools, SUPERUSER_ID
from openerp import fields
from openerp.addons.website.models.website import slug
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _
from openerp.addons.auth_signup.controllers.main import AuthSignupHome as Home
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class hms_portal(http.Controller):
    @http.route(['/my/account'], type='http', auth="user", website=True)
    def my_account(self, **kw):
        partner = request.env.user.partner_id
        
        # get customer sales rep
        if partner.user_id:
            sales_rep = partner.user_id
        else:
            sales_rep = False
        response = {
            'sales_rep': sales_rep,
            'company': request.website.company_id,
            'user': request.env.user
        }
        
        partner = request.env.user.partner_id

        res_patient = request.env['hms.patient']
        res_appointment = request.env['hms.appointment']
        res_invoices = request.env['account.invoice']
        patient = res_patient.search([
            ('partner_id.id', '=', partner.id),
        ])
        
        apps = res_appointment.search([
            ('patient_id.id', '=', patient.id),
        ])
        invoices = res_invoices.search([
            ('partner_id.id', '=', partner.id),
            ('state', 'in', ['open', 'paid', 'cancelled'])
        ])

        response.update({
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'patient': patient,
            'apps': apps,
            'invoices': invoices,
        })
        return request.website.render("hms_portal.myaccount", response)
        
    @http.route(['/create/appointment'], type='http', auth='user', website=True)
    def create_appointment(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }
        
        slots = request.env['appointment.schedual.slot'].sudo().search([('slot_date','>=',datetime.datetime.now().date().strftime('%Y-%m-%d'))])
        slot_lines = request.env['appointment.schedual.slot.lines'].sudo().search([])
	department_ids = request.env['hospital.department'].sudo().search([])
        
        values.update({
            'slots': slots,
            'slot_lines': slot_lines,
            'partner': partner,
            'redirect': redirect,
	    'department_id': department_ids,
        })

        return request.website.render("hms_portal.appointment_details", values)
        
    @http.route(['/save/appointment'], type='http', auth='user', website=True)
    def save_appointment(self, redirect=None, **post):
        env = request.env
        partner = env['res.users'].browse(request.uid).partner_id
        app_obj = env['hms.appointment']
        res_patient = env['hms.patient']
        slot_line = env['appointment.schedual.slot.lines']
        user = env.user.sudo()
        values = {
            'error': {},
            'error_message': [],
            'partner': partner,
        }
        
        patient = res_patient.search([('partner_id.id', '=', partner.id)],limit=1)
        slot = slot_line.browse(int(post.get('slot_lines')))
        dept = post.get('department_id', '')
        if post.get('department_id', ''):
            dept = int(post.get('department_id', ''))
        
        if post:
            now = datetime.datetime.now()
            user_tz = pytz.timezone(request.context.get('tz') or env.user.tz or 'UTC')
            app_date = user_tz.localize(datetime.datetime.strptime(slot.from_slot, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(pytz.utc)
            app_date.replace(tzinfo=None)
            
            if app_date.replace(tzinfo=None) < now:
                values.update({'error_message':['Appointment date is past please enter valid.']})
                return request.website.render("hms_portal.appointment_details", values)
                
            error, error_message = self.details_application_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            
            if not error:
                post.update({'schedual_slot_id':slot.id,'booked_online':True,'patient_id': patient.id, 'date': app_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
                patient.sudo().write({'name':post.pop('name', ''),'department_id': dept,'mobile':post.pop('mobile', '')})
                user.sudo().write({'department_ids':[(4,[dept])]})
                # Create Appointment
                app_id = app_obj.sudo().create(post)
                app_id.create_invoice()
                app_id.invoice_id.signal_workflow('invoice_open')
                invoice = app_id.invoice_id
                
                acquirer_id = env['ir.values'].get_default('payment.acquirer', 'acquirer_id') or \
                env['payment.acquirer'].search([('website_published', '=', True)])[0].id
                acquirer = env['payment.acquirer'].with_context(submit_class='btn btn-primary pull-right',
                                                        submit_txt=_('Pay Now')).browse(acquirer_id)
                pay_val = {'reference':invoice.number,'amount':invoice.amount_total,'acquirer': acquirer,'currency': user.company_id.currency_id}
                #return request.website.render('website_payment.pay', pay_val)
                
                return request.redirect('/website_payment/pay?reference=%s&amount=%s&currency_id=%s&country_id=%s' %(invoice.number,invoice.amount_total,invoice.currency_id.id,invoice.partner_id.country_id.id))

        return request.redirect('/my/account')
        
    def details_form_validate(self, data):
        error = dict()
        error_message = []

        mandatory_billing_fields = ["mobile","email"]

        # Validation
        for field_name in mandatory_billing_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))
        return error, error_message
        
    def details_application_validate(self, data):
        error = dict()
        error_message = []

        mandatory_billing_fields = ["name", "mobile","slot_lines"]

        # Validation
        for field_name in mandatory_billing_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))
        return error, error_message
        
        
    @http.route(['/my/change/load'], type='http', auth='user',website=True)
    def change_details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }
        
        states = request.env['res.country.state'].sudo().search([])
        countries = request.env['res.country'].sudo().search([])

        values.update({
            'partner': partner,
            'states': states,
            'countries': countries,
            'redirect': redirect,
        })

        return request.website.render("hms_portal.change_details", values)

    @http.route(['/my/change'], type='http', auth='user',website=True)
    def change_my_details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        
        res_patient = request.env['hms.patient']
        patient = res_patient.search([
            ('partner_id.id', '=', partner.id),
        ],limit=1)
        
        values = {
            'error': {},
            'error_message': []
        }
        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                post.update({'zip': post.pop('zipcode', ''),'mobile': post.pop('mobile', ''),'country_id': post.pop('countries', ''),'state_id': post.pop('states', '')})
                patient.sudo().write(post)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/change')

        values.update({
            'partner': partner,
            #'country_id': countries.id,
            #'state_id': states.id,
            'redirect': redirect,
        })

        return request.redirect('/my/account')
        
class HmsAuthLogin(Home):

    def do_signup(self, qcontext):
        values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password','mobile'))
        assert any([k for k in values.values()]), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."
        supported_langs = [lang['code'] for lang in request.registry['res.lang'].search_read(request.cr, SUPERUSER_ID, [], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.cr.commit()
        print "==========================="
        
        
    
