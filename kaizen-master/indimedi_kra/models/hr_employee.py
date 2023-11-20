from openerp import api, models, fields
from datetime import datetime,date
from openerp import tools

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    salary_of_oneday = fields.Float(compute="_count_one_day_salary",string="One day salary")
    remain_salary = fields.Float(compute="_remain_salary_with_last_day",string="Remain salary with last day")
    number_of_days = fields.Float(compute="_remain_salary_with_last_day",string="Number of days")
    salary_start_date = fields.Date(string="Last Salary Start Day")
    cheque_no = fields.Char(string="Cheque No.")
    cheque_date = fields.Date(string="Cheque Date")


    @api.multi
    def _count_one_day_salary(self):
        for salary in self.contract_ids:
            if salary.state == 'open':
                if salary.schedule_pay == 'monthly':
                    self.salary_of_oneday = salary.wage/30.0
                elif salary.schedule_pay == 'quarterly':
                    self.salary_of_oneday = salary.wage/91.0
                elif salary.schedule_pay == 'semi-annually':
                    self.salary_of_oneday = salary.wage/180.0
                elif salary.schedule_pay == 'annually':
                    self.salary_of_oneday = salary.wage/365.0
                elif salary.schedule_pay == 'weekly':
                    self.salary_of_oneday = salary.wage/7.0
                elif salary.schedule_pay == 'bi-weekly':
                    self.salary_of_oneday = salary.wage/14.0
                elif salary.schedule_pay == 'bi-monthly':
                    self.salary_of_oneday = salary.wage/60.0


    @api.depends('salary_of_oneday','resignation_date','last_date')
    def _remain_salary_with_last_day(self):


        fmt = '%Y-%m-%d'
        if self.salary_start_date and self.last_date:
            d1 = datetime.strptime(self.salary_start_date, fmt)
            d2 = datetime.strptime(self.last_date, fmt)
            daysDiff = float((d2-d1).days)
            self.number_of_days = daysDiff
            self.remain_salary = self.salary_of_oneday*daysDiff
    