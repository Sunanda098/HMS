# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from openerp import fields, models, api, SUPERUSER_ID
from openerp.tools.translate import _
from datetime import datetime
from openerp.exceptions import UserError, ValidationError


class IndimediDMS(models.Model):
    _name = "indimedi.survey"
    _rec_name = "employee_id"
    _inherit = "mail.thread"
    _description = "Employee Review"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    user_id = fields.Many2one('hr.employee', 'Manager')
    survey_id = fields.Many2one('survey.survey', 'Survey')
    state = fields.Selection([('new', 'New'), ('progress', 'In Progress'), ('done', 'Done')], default="new")

    def _employee_survey_create(self, cr, uid, context=None):
        employee_obj = self.pool.get('hr.employee')
        employee_id = employee_obj.search(cr, uid, [], context=context)
        employees = employee_obj.browse(cr, uid, employee_id, context=context)
        template = False
        try:
            template = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'indimedi_survey', 'hr_evaluation_notification')
        except:
            pass
        for employee in employees:
            diff = datetime.now() - datetime.strptime(employee.create_date, '%Y-%m-%d %H:%M:%S')
            if diff.days == 7 and employee.survey_one and employee.department_id.manager_id.id:
                self.create(cr, SUPERUSER_ID, {
                    'employee_id': employee.id,
                    'user_id': employee.department_id.manager_id.id,
                    'survey_id': employee.survey_one.id or None,
                    'state': 'progress',
                })
                if template and employee.department_id.manager_id.id:
                    self.pool.get('mail.template').send_mail(cr, SUPERUSER_ID, template.id, employee.department_id.manager_id.id, force_send=True, raise_exception=True, context=context)
            elif diff.days == 15 and employee.survey_two and employee.department_id.manager_id.id:
                self.create(cr, SUPERUSER_ID, {
                    'employee_id': employee.id,
                    'user_id': employee.department_id.manager_id.id,
                    'survey_id': employee.survey_two.id or None,
                    'state': 'progress',
                })
                if template and employee.department_id.manager_id.id:
                    self.pool.get('mail.template').send_mail(cr, SUPERUSER_ID, template.id, employee.department_id.manager_id.id, force_send=True, raise_exception=True, context=context)
            elif diff.days == 30 and employee.survey_three and employee.department_id.manager_id.id:
                self.create(cr, SUPERUSER_ID, {
                    'employee_id': employee.id,
                    'user_id': employee.department_id.manager_id.id,
                    'survey_id': employee.survey_three.id or None,
                    'state': 'progress',
                })
                if template and employee.department_id.manager_id.id:
                    self.pool.get('mail.template').send_mail(cr, SUPERUSER_ID, template.id, employee.department_id.manager_id.id, force_send=True, raise_exception=True, context=context)

    @api.multi
    def action_review_answer(self):
        return self.survey_id.action_start_survey()

    @api.multi
    def action_done(self):
        return self.write({'state': 'done'})

    @api.multi
    def action_result(self):
        return {
            'name': 'Result',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'survey.user_input',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': ['&', ('survey_id', '=', self.survey_id.id),('partner_id', '=', self.user_id.user_id.partner_id.id)],
            'context': self._context,
        }

    def action_send(self, cr, uid, ids, context=None):
        template = False
        survey_id = self.browse(cr, uid, ids, context=context)
        try:
            template = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'indimedi_survey', 'hr_evaluation_notification')
        except:
            pass
        if template and survey_id.employee_id.parent_id.id:
            self.pool.get('mail.template').send_mail(cr, uid, template.id, survey_id.employee_id.parent_id.id, force_send=True, raise_exception=True, context=context)
        return self.write(cr, uid, ids, {'state': 'progress'}, context=context)

class HR(models.Model):
    _inherit = 'hr.employee'

    # @api.model
    # def create(self, vals):
    #     emp_id = super(HR, self).create(vals)
    #     if not emp_id.company_id.email_tem_id:
    #         raise ValidationError(_('Please select email template for employee notification in company->templates.'))
    #     project_id = False
    #     data_obj = self.env['ir.model.data']
    #     task_obj = self.env['project.task']
    #     try:
    #         project_id = data_obj.get_object('indimedi_survey', 'hr_employee_project')
    #     except:
    #         pass
    #     self.pool.get('mail.template').send_mail(self._cr, self._uid, emp_id.company_id.email_tem_id.id, emp_id.id, force_send=True, raise_exception=True, context={})
    #     task_obj.create({
    #         'name': emp_id.name,
    #         'project_id': project_id and project_id.id or False,
    #         'user_id': emp_id.user_id and emp_id.user_id.id or False,
    #         #'responsible_ids': [(4, emp_id.parent_id.user_id.id)],
    #     })
    #     return emp_id


    def write(self, cr, uid, ids, vals, context={}):
        res = super(HR, self).write(cr, uid, ids, vals, context=context)
        if vals.get('user_id'):
            for emp in self.browse(cr, uid, ids, context=context):
                template = False
                project_id = False
                data_obj = self.pool['ir.model.data']
                task_obj = self.pool['project.task']
                try:
                    template = data_obj.get_object(cr, uid, 'indimedi_survey', 'hr_employee_dir_notification', context=context)
                    project_id = data_obj.get_object(cr, uid, 'indimedi_survey', 'hr_employee_project', context=context)
                except:
                    pass
                self.pool.get('mail.template').send_mail(cr, uid, template.id, emp.id, force_send=True, raise_exception=True, context=context)
                task_obj.create(cr, uid, {
                    'name': emp.name,
                    'project_id': project_id and project_id.id or False,
                    'user_id': emp.user_id and emp.user_id.id or False,
                    #'responsible_ids': [(4, self.parent_id.user_id.id)],
                }, context=context)
        return res


class ResCompany(models.Model):
    _inherit = "res.company"

    email_tem_id = fields.Many2one('mail.template', 'Employee Template')
        

