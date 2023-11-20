from openerp import api, models, fields

class HrEmployee(models.Model):
	_inherit = "hr.employee"

	# _columns = {
	salary_of_oneday = fields.Float(string="One day salary")
	# }

	# @api.onchange('resignation_date','last_date')
	# def _count_one_day_salary(self):
	# 	sal = self.resignation_date - self.last_date
	# 	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",sal.days())
	# 	for salary in contract_ids:
	# 		if salary.state == 'open':
	# 			if salary.schedule_pay == 'monthly':
	# 				self.salary_of_oneday = salary.wage/30.0
	# 			elif salary.schedule_pay == 'quarterly':
	# 				self.salary_of_oneday = salary.wage/91.0
	# 			elif salary.schedule_pay == 'semi-annually':
	# 				self.salary_of_oneday = salary.wage/180.0
	# 			elif salary.schedule_pay == 'annually':
	# 				self.salary_of_oneday = salary.wage/365.0
	# 			elif salary.schedule_pay == 'weekly':
	# 				self.salary_of_oneday = salary.wage/7.0
	# 			elif salary.schedule_pay == 'bi-weekly':
	# 				self.salary_of_oneday = salary.wage/14.0
	# 			elif salary.schedule_pay == 'bi-monthly':
	# 				self.salary_of_oneday = salary.wage/60.0

