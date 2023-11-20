# -*- coding: utf-8 -*-
import datetime
import time
from openerp.osv import osv, orm, fields
from openerp import api, _
#from openerp.addons.base.ir.ir_qweb import HTMLSafe

from openerp.exceptions import UserError, ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DS
from datetime import datetime,date
from dateutil.relativedelta import relativedelta


mapping = ['sys_process','follow_instr','flexible','plan','job_knowledge','skill','learn_skill','accuracy','reliability','cust_sati','work_comple','pressure','handling','relationship','prob_solv','dec_mak','time_mng','express','share_know',
              'seeks','open_ideas','enthu','trust','ettiquttes','punctuality','descipline','attendance','team_work','team_build','strategy', 'participation']
mapping_avg = ['sys_process','follow_instr','flexible','plan','job_knowledge','skill','learn_skill','accuracy','reliability','cust_sati','work_comple','pressure','handling']


class HRHolidays(osv.osv):
    _inherit = 'hr.holidays'

    def _create_leave_employee_per_month(self, cr, uid, context=None):
        employee_obj = self.pool.get('hr.employee')
        model_data_obj = self.pool.get('ir.model.data')
        data_id = model_data_obj.search(cr, uid, [('name', '=', 'employee_tag_probation')], limit=1, context=context)
        probation_tag = model_data_obj.browse(cr, uid, data_id, context=context)
        holidays_type_id = model_data_obj.search(cr, uid, [('name', '=', 'holiday_status_cl')], limit=1, context=context)
        holidays_type = model_data_obj.browse(cr, uid, holidays_type_id, context=context)
        employee_ids = employee_obj.search(cr, uid, [('category_ids', '!=', probation_tag.res_id)], context=context)
        for emp_id in employee_ids:
            self.create(cr, uid, {
                'name': 'Per Month Employee Leave',
                'holiday_status_id': holidays_type.res_id,
                'holiday_type': 'employee',
                'employee_id': emp_id,
                'number_of_days_temp': 1,
                'state': 'draft',
                'type': 'add',
            }, context)

class hr_job(osv.osv):
    _inherit = 'hr.job'

    _columns = {
        'kra_id': fields.many2one('indimedi.kra', 'KRA'),
    }


employee_progress_fields = ['nda_sign', 'background_check', 'verify_check', 'group_broad', 'alternate_phone_no', 'alternate_email_id', 'verification', 'background_check_details',
'esci', 'pf_form', 'bank_acc', 'cheque_scanned', 'nda' , 'final_degree', 'card_no', 'biometric', 'Spark_id', 'skype', 'e_mail', 'computer_allocated',
'is_experience', 'is_experience', 'address_proof', 'id_proof']

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
        

    # _columns = {
    #     'date_joining': fields.date('Date of joining'),
    # }


    def _document_count(self, cr, uid, ids, field_name, arg, context=None):
        kra_ids = self.pool.get('employee.kra').search(cr, uid, [('employee_id', 'in', ids)])
        res = {}
        res[ids[0]] = len(kra_ids)
        return res

    def _survey_count(self, cr, uid, ids, field_name, arg, context=None):
        survey_ids = self.pool.get('indimedi.survey').search(cr, uid, [('employee_id', 'in', ids)])
        res = {}
        res[ids[0]] = len(survey_ids)
        return res

    def _employee_joining_progress(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        todo = len('employee_progress_fields')
        for employee in self.browse(cr, uid, ids, context=context):
            done = 0
            for field in employee_progress_fields:
                if employee[field]:
                    done += 1 
            res[employee.id] = {
                'employee_joining_progress': ( 100 * done ) / todo,
                'color': 3 if done<todo else 0,
            }
        return res

    _columns = {
        'kra_id': fields.related('job_id', 'kra_id', type='many2one', relation='indimedi.kra', string="KRA", readonly=True),
        'employee_code': fields.integer('Employee Code', required=True),
        'kra_count': fields.function(_document_count, type='integer', string="KRA"),
        'mobile_alternative': fields.char("Alternate Mobile"),
        #exit  checklist
        'super_approval': fields.boolean("Did Supervisor Approved resignation by replying to employee mail and CC to HR?"),
        'is_notice': fields.boolean("Is notice period mentioned on email?"),
        'is_resource': fields.boolean("Have we given any resource to him? Has he submitted that back to company?\
                                        (headphone,simcard, ID card, etc)"),
        'cheque_received': fields.boolean("Cheque Receipt received?"),
        'security_cheque': fields.boolean("Security cheque given back?"),
        'loan_paid': fields.boolean("All loan paid?"),
        'pf_nos': fields.boolean("PF no. given to emp?"),
        'esi_nos': fields.boolean("ESI no. given to emp?"),
        'is_tds': fields.boolean("TDS need to cut?"),
        'tds_certificate': fields.boolean("TDS certificate given?"),
        'experience_letter': fields.boolean("Experience letter must be as per he worked for company"),
        'is_notice': fields.boolean("Has he/she completed notice period time?"),
        'non_due': fields.boolean("Non Due Certificate signed"),        
        'is_pwd_chng': fields.boolean("Have we changed basecamp, skype, mail pwd, ERP, \
                                        any access given from 3rd party, fmv, client site pwd change?"),
        'resignation_date': fields.date("Resignation date"),
        'last_date': fields.date("Last Date in organization"),
#Joining check list
        'id_proof': fields.boolean("ID Proof"),
        'address_proof': fields.boolean("Address Proof"),
        'is_experience': fields.boolean("If he has experience then Experience letter"),
        'computer_allocated': fields.char("Computer alloted no"),
        'e_mail': fields.char("Elsner Mail id"),
        'skype': fields.char("Elsner Skype"),
        'Spark_id': fields.char("Spark Id"),
        'biometric': fields.char("Biomatric code"),
        'card_no': fields.char("Access card code no"),
        'final_degree': fields.boolean("Final degree copy"),
        'nda': fields.boolean("NDA "),
        'cheque_scanned': fields.char("Cheque Scanned copy"),
        'bank_acc': fields.char("Bank Account no"),
        'pf_form': fields.boolean("PF form 11"),
        'esci': fields.char("ESIC"),
        'background_check_details': fields.char("Background Check Details"),
        'verification': fields.char("With whom spoek for background verification"),
        'alternate_email_id': fields.char("Alternate email id"),
        'alternate_phone_no': fields.char("Alternate phone no"),
        'group_broad': fields.boolean("New Employee added in Group broad cast?"),
        'verify_check': fields.boolean("Did you Verify home and other phone no?"),
        'background_check': fields.boolean("Background Check ?"),
        'nda_sign': fields.boolean("NDA sign"),
        'employee_joining_progress': fields.function(_employee_joining_progress, multi="color", type='integer', string="Progress"),
        'color': fields.function(_employee_joining_progress, multi="color", type='integer', string="Progress"),
        'pan_card': fields.char("Pan Card"),
        'survey_one': fields.many2one('survey.survey', 'Survey for 7 Days'),
        'survey_two': fields.many2one('survey.survey', 'Survey for 15 Days'),
        'survey_three': fields.many2one('survey.survey', 'Survey for 30 Days'),
        'survey_count': fields.function(_survey_count, type='integer', string="Survey"),
        # 'date_joining': fields.date('Joining Date', required=True),
        # 'date_joining': fields.date('Joining Date', required=True),
        'three_months_after': fields.date(),
        'job_id': fields.many2one('hr.job', 'Job Title', required=True),
    }

    @api.onchange('date_joining')
    def _depends_doc(self):
        if self.date_joining:
            self.three_months_after = datetime.strptime(self.date_joining, DS) + relativedelta(months=3)

    def action_kra_tree_view(self, cr, uid, ids, context=None):
        return {
            'name': 'Employee KRA',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'employee.kra',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('employee_id', 'in', ids)],
            'context': context,
        }

    def action_survey_tree_view(self, cr, uid, ids, context=None):
        return {
            'name': 'Employee Survey',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'indimedi.survey',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('employee_id', 'in', ids)],
            'context': context,
        }

    @api.multi
    def toggle_active(self):
        cols = ['super_approval', 'is_notice', 'is_resource',
            'cheque_received', 'security_cheque', 'loan_paid',
            'pf_nos', 'is_tds', 'tds_certificate',
            'experience_letter', 'is_notice', 'non_due', 'is_pwd_chng',
        ]
        for col in cols:
            if not eval('self.'+col):
                raise ValidationError(_('Please select %s.')%(col))
        super(hr_employee, self).toggle_active()

class employee_kra(osv.osv):
    _name = 'employee.kra'
    _inherit = ['mail.thread']
    _columns = {
        'name': fields.selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'october'), (11, 'November'), (12, 'December') ], "KRA Month"),
        'quarterly': fields.selection([(1, 'First Quarter'), (2, 'Second Quarter'), (3, 'Third Quarter'), (4, 'Fourth Quarter')], "KRA Quarter"),
        'year': fields.many2one('indimedi.year', 'Year'),
        'employee_id': fields.many2one('hr.employee', 'Employee'),
        'kra_id': fields.related('employee_id', 'kra_id', type='many2one', relation='indimedi.kra', string="KRA", readonly=True),
        'kra_question_ids':fields.one2many('employee.kra.question', 'employee_kra_id', 'KRA Question'),
        'date': fields.date("Date"),
        'state': fields.selection([('draft', 'Draft'), ('submit', 'Submit To Supervisor'), ('cancel', 'Cancelled'), ('done', 'Done'), ], "State", track_visibility='onchange'),
    }
    _defaults = {
       'date': fields.date.context_today,
       'state':'draft'
       }

    def action_submit(self, cr, uid, ids, employee_id, context=None):
        return self.write(cr, uid, ids, {'state':'submit'}, context=context)

    def action_cancel(self, cr, uid, ids, employee_id, context=None):
        return self.write(cr, uid, ids, {'state':'cancel'}, context=context)

    def action_done(self, cr, uid, ids, employee_id, context=None):
        return self.write(cr, uid, ids, {'state':'done'}, context=context)

    def onchange_employee_id(self, cr, uid, ids, employee_id, context=None):
        res = {'value': {}}
        employee = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
        kra_obj = self.pool.get('kra.question')
        que_ids = kra_obj.search(cr, uid, [('kra_id', '=', employee.job_id.kra_id.id)], context=context)
        que_records = kra_obj.browse(cr, uid, que_ids, context=context)
        data = []
        que_obj = self.pool.get('employee.kra.question')
        for que in que_records:
            data.append(que_obj.create(cr, uid, {'employee_id':employee_id, 'name':que.question, 'weightage':que.weightage, 'kra_question_id':que.id, 'employee_kra_id':ids and ids[0] or False,
                'hint':que.name}, context=context))
        return {'value': {'kra_question_ids': data}}

class employee_kra_question(osv.osv):
    _name = 'employee.kra.question'

    def _compute_total(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for que in self.browse(cr, uid, ids, context=context):
            res[que.id] = (que.weightage * que.manager_rating) / 10
        return res

    def _check_max_limit(self, cr, uid, ids, context=None):
        for que in self.browse(cr, uid, ids, context=context):
             if (que.employee_rating < 0.0 or que.employee_rating > 10.0):
                 return False
             if (que.manager_rating < 0.0 or que.manager_rating > 10.0):
                 return False
        return True

    def _get_updated_rating(self, cr, uid, ids, context=None):
        return ids

    _columns = {
        'name': fields.char('Employee KRA'),
        'employee_kra_id': fields.many2one('employee.kra', 'KRA'),
        'employee_id': fields.many2one('hr.employee', string="Employee"),
        'kra_question_id': fields.many2one('kra.question', 'Question'),
        'hint': fields.char('Hint'),
        'employee_remark': fields.char('Employee Remark'),
        'manager_remark': fields.char('Manager Remark'),
        'employee_rating': fields.float('Employee Rating'),
        'manager_rating': fields.float('Manager Rating'),
        'weightage': fields.integer('Weightage'),
        'final_score': fields.function(_compute_total, string='Final Score', type="float", store={
              'employee.kra.question': (_get_updated_rating, ['manager_rating'], 10),
        }),
    }

    _defaults = {
         'state':'draft',
     }

    _constraints = [
        (_check_max_limit, 'Rating in between 0-10 only', ['employee_rating', 'manager_rating'])]

class indimedi_kra(osv.osv):
    _name = 'indimedi.kra'
    _inherit = ['mail.thread']
    def _check_allocation(self, cr, uid, ids, context=None):
        total = 0.0
        for percentage in self.browse(cr, uid, ids, context=context):
            for amount in percentage.kra_question_ids:
                total += amount.weightage
            if total == 100 or total == 0:
                return True
        return False

    _columns = {
        'name': fields.char('Name'),
        'kra_question_ids':fields.one2many('kra.question', 'kra_id', 'KRA Question'),
    }

    _constraints = [
            (_check_allocation, 'Warning!| The total Weightage distribution should be 100%.', ['kra_question_ids']), ]

class kra_question(osv.osv):
    _name = 'kra.question'
    _rec_name = 'question'

    _columns = {
        'kra_id': fields.many2one('indimedi.kra', 'KRA'),
        'question': fields.char('Question'),
        'name': fields.char('Hint'),
        'description': fields.text('Description'),
        'weightage': fields.integer('Weightage'),
        'sequence': fields.char('Sr.No'),
    }

class value_rating(osv.osv):
    _name = 'value.rating'
    _inherit = ['mail.thread']

    def _check_max_limit(self, cr, uid, ids, context=None):
        for values in self.browse(cr, uid, ids, context=context):
            for val in mapping:
                if (values[val] < 0.0 or values[val] > 5.0):
                 return False
        return True

    def calculate_avg(self, cr, uid, ids, context=None):
        res = 0.0
        for values in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for val in mapping_avg:
                total += values[val]
            res =  total /len(mapping_avg)
        return res

    def total_average(self, cr, uid, ids,context=None):
        res = 0.0
        for values in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for val in mapping:
                total += values[val]
            res =  total /len(mapping)
        return res

    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee Name'),
        # 'employee_code': fields.related('employee_id', 'employee_code', type='integer', string="Employee Code" ,readonly=True),
        'month':fields.selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
                                  (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], 'Month'),
        'year': fields.many2one('indimedi.year', 'Year'),
        'designation': fields.many2one('indimedi.kra', 'Designation'),
        'appraiser_id': fields.related('employee_id', 'parent_id', type='many2one', relation='hr.employee', string="Appraiser", store=True),
        'sys_process': fields.float('System and Processes'),
        'follow_instr': fields.float('Follow Instructions'),
        'flexible': fields.float('Adaptable and Flexible'),
        'plan': fields.float('Ability To Plan'),
        'job_knowledge': fields.float('Job Knowledge'),
        'skill': fields.float('Skill To Handle Work'),
        'learn_skill': fields.float('Learn New Skill'),
        'accuracy': fields.float('Accuracy'),
        'reliability': fields.float('Reliability'),
        'cust_sati': fields.float('Client Satisfaction'),
        'work_comple': fields.float('Work Completion On Time'),
        'pressure': fields.float('Ability to work under pressure'),
        'handling': fields.float('Handling new portfolio'),
        'score_leader': fields.function(calculate_avg , 'Score leadership'),
        'relationship': fields.float('Relationship with co-workers'),
        'prob_solv': fields.float('Problem solving'),
        'dec_mak': fields.float('Decision making'),
        'time_mng': fields.float('Time management'),
        'express': fields.float('Oral and written expression'),
        'share_know': fields.float('Sharing of knowledge'),
        'seeks': fields.float('Seeks T & D'),
        'open_ideas': fields.float('Open to ideas'),
        'enthu': fields.float('Enthusiastic'),
        'trust': fields.float('Trustworthy'),
        'ettiquttes': fields.float('Work Place ettiquttes'),
        'punctuality': fields.float('Punctuality'),
        'descipline': fields.float('Descipline'),
        'attendance': fields.float('Attendance'),
        'team_work': fields.float('Team work'),
        'team_build': fields.float('Team Building'),
        'strategy': fields.float('New Strategy and direction'),
        'participation': fields.float('Participation in HR activities'),
        'total_avg': fields.function(total_average , 'Total average'),
        'state': fields.selection([('draft', 'Draft'), ('submit', 'Submit To Supervisor'), ('cancel', 'Cancelled'), ('done', 'Done'), ], "State" ,track_visibility='onchange'),
    }

    _defaults = {
       'state':'draft'
       }

    _constraints = [
        (_check_max_limit, 'Value Rating in between 0-5 only', ['sys_process','follow_instr','flexible','plan','job_knowledge','skill','learn_skill','accuracy','reliability','cust_sati','work_comple','pressure','handling','relationship','prob_solv','dec_mak','time_mng','express','share_know',
                                                                'seeks','open_ideas','enthu','trust','ettiquttes','punctuality','descipline','attendance','team_work','team_build','strategy', 'participation']),
    ]

    def action_submit(self, cr, uid, ids, employee_id, context=None):
        return self.write(cr, uid, ids, {'state':'submit'}, context=context)

    def action_cancel(self, cr, uid, ids, employee_id, context=None):
        return self.write(cr, uid, ids, {'state':'cancel'}, context=context)

    def action_done(self, cr, uid, ids, employee_id, context=None):
        return self.write(cr, uid, ids, {'state':'done'}, context=context)


class indimedi_year(osv.osv):
    _name = 'indimedi.year'

    _columns = {
        'name': fields.char('Year', size=4),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
