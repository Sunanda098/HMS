# coding=utf-8
from openerp import api, fields, models
from openerp.tools.translate import _
from datetime import datetime
from openerp.tools.safe_eval import safe_eval as eval
from openerp.exceptions import UserError, ValidationError


class hr_contract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = 'hr.contract'
    _description = 'Employee Contract'


    date_contract = fields.Date(required=True, index=True, copy=False, default=fields.Date.context_today)
    ctc_amount = fields.Float(string="CTC Amount")



    @api.onchange('wage')
    def onchange_wage(self):
        if self.wage:
            self.ctc_amount = float(12 * float(self.wage))

    @api.multi
    def com(self):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            if category.code in localdict['categories'].dict:
                amount += localdict['categories'].dict[category.code]
            localdict['categories'].dict[category.code] = amount
            return localdict

        class BrowsableObject(object):
            def __init__(self, pool, cr, uid, employee_id, dict):
                self.pool = pool
                self.cr = cr
                self.uid = uid
                self.employee_id = employee_id
                self.dict = dict

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0
        
        result_dict = {}
        categories_dict = {}
        rules = {}
        blacklist = []
        categories_obj = BrowsableObject(self.pool, self.env.cr, self.env.uid, self.employee_id.id, categories_dict)
        rules_obj = BrowsableObject(self.pool, self.env.cr, self.env.uid, self.employee_id.id, rules)
        
        baselocaldict = {'categories': categories_obj, 'rules': rules_obj}

        structure_ids = self.struct_id or False
        rule_ids = self.pool.get('hr.payroll.structure').get_all_rules(self.env.cr, self.env.uid, structure_ids.ids)
        # rule_ids = self.struct_id and self.struct_id.rule_ids.ids or []
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]

        obj_rule = self.pool.get('hr.salary.rule')

        for contract in self:
            employee = contract.employee_id
            localdict = dict(baselocaldict, employee=employee, contract=contract)
            for rule in obj_rule.browse(self.env.cr, self.env.uid, sorted_rule_ids):
                key = rule.code + '-' + str(contract.id)
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                localdict['result_rate'] = 100
                #check if the rule can be applied
                if obj_rule.satisfy_condition(self.env.cr, self.env.uid, rule.id, localdict) and rule.id not in blacklist:
                    #compute the amount of the rule
                    amount, qty, rate = obj_rule.compute_rule(self.env.cr, self.env.uid, rule.id, localdict, context=self.env.context)
                    print "----------amount,$$$$$-qty----------",amount,qty,rate
                    #check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #set/overwrite the amount computed for this rule in the localdict
                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules[rule.code] = rule

                    # ctc_amount = float(12 * float(self.wage))
                    #sum the amount for its salary category
                    print rule.amount_percentage,rule.amount_fix,rule.amount_python_compute
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    totals = float(qty) * amount * rate / 100
                    #create/overwrite the rule in the temporary results
                    result_dict[key] = {
                        # 'salary_rule_id': rule.id,
                        # 'contract_id': contract.id,
                        # 'name': rule.name,
                        # 'code': rule.code,
                        'category':rule.category_id.name,
                        'category_id': rule.category_id.id,
                        # 'sequence': rule.sequence,
                        # 'appears_on_payslip': rule.appears_on_payslip,
                        # 'condition_select': rule.condition_select,
                        # 'condition_python': rule.condition_python,
                        # 'condition_range': rule.condition_range,
                        # 'condition_range_min': rule.condition_range_min,
                        # 'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        # 'amount_fix': rule.amount_fix,
                        # 'amount_python_compute': rule.amount_python_compute,
                        # 'amount_percentage': rule.amount_percentage,
                        # 'amount_percentage_base': rule.amount_percentage_base,
                        # 'register_id': rule.register_id.id,
                        'amount': amount,
                        'totals': totals,
                        'employee_id': contract.employee_id.id,
                        'quantity': qty,
                    }
                # else:
                #     #blacklist this rule and its children
                #     blacklist += [id for id, seq in self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]

        result = [value for code, value in result_dict.items()]
        print "------------------------------------------------------",result
        return result

    @api.multi
    def _get_amount_result(self):

        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            if category.code in localdict['categories'].dict:
                amount += localdict['categories'].dict[category.code]
            localdict['categories'].dict[category.code] = amount
            return localdict

        class BrowsableObject(object):
            def __init__(self, pool, cr, uid, employee_id, dict):
                self.pool = pool
                self.cr = cr
                self.uid = uid
                self.employee_id = employee_id
                self.dict = dict

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        result_dict = {}
        categories_dict = {}
        dict_1 = {}
        result = []
        rules = {}
        blacklist = []
        categories_obj = BrowsableObject(self.pool, self.env.cr, self.env.uid, self.employee_id.id, categories_dict)
        rules_obj = BrowsableObject(self.pool, self.env.cr, self.env.uid, self.employee_id.id, rules)
        
        baselocaldict = {'categories': categories_obj, 'rules': rules_obj}

        structure_ids = self.struct_id or False
        rule_ids = self.pool.get('hr.payroll.structure').get_all_rules(self.env.cr, self.env.uid, structure_ids.ids)
        # rule_ids = self.struct_id and self.struct_id.rule_ids.ids or []
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]

        obj_rule = self.pool.get('hr.salary.rule')
        key = 0
        for contract in self:
            employee = contract.employee_id
            localdict = dict(baselocaldict, employee=employee, contract=contract)
            for rule in obj_rule.browse(self.env.cr, self.env.uid, sorted_rule_ids):
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                localdict['result_rate'] = 100
                #check if the rule can be applied
                if obj_rule.satisfy_condition(self.env.cr, self.env.uid, rule.id, localdict) and rule.id not in blacklist:
                    #compute the amount of the rule
                   
                    amount, qty, rate = obj_rule.compute_rule(self.env.cr, self.env.uid, rule.id, localdict, context=self.env.context)
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #set/overwrite the amount computed for this rule in the localdict
                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules[rule.code] = rule

                    # ctc_amount = float(12 * float(self.wage))
                    #sum the amount for its salary category
                    print rule.amount_percentage,rule.amount_fix,rule.amount_python_compute
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    totals = float(qty) * amount * rate / 100
                    dict_1[key]={'amount':amount,'qty':qty,'rate':rate,'name': rule.name,'amount_select': rule.amount_select,'category':rule.category_id.name,'category_id': rule.category_id.id,}
                    key += 1

        result = [value for code, value in dict_1.items()] 
        print "--------------------$$$----------------------------------",result
        return result

    @api.multi
    def compute_rule(self, rule, localdict):
        """
        :param rule_id: id of rule to compute
        :param localdict: dictionary containing the environement in which to compute the rule
        :return: returns a tuple build as the base/amount computed, the quantity and the rate
        :rtype: (float, float, float)
        """
        # import pdb
        # pdb.set_trace()
        # rule = self.env['hr.salary.rule'].browse(rule_id)

        # print "\n\nRule.......................",rule
        # print "rule.amount_fix, rule.quantity. localdict .......................",rule.amount_fix, " ---- ", rule.quantity, " ---- ",  localdict
        # print "Rule.......................", rule.amount_select
        # print "eval ", rule.amount_percentage_base, " >>>>> ", rule.quantity, " >>>>>>>>>>> ", rule.amount_percentage
        # print " Python COmpute >>>>>>>>>> ", rule.amount_python_compute

        if rule.amount_select == 'fix':
            try:
                # print  "before return........",rule.amount_fix, float(eval(rule.quantity, localdict)), 100.0 
                return rule.amount_fix, float(eval(rule.quantity, localdict)), 100.0
            except:
                raise UserError(_('Wrong quantity defined for salary rule %s (%s).') % (rule.name, rule.code))
        elif rule.amount_select == 'percentage':
            try:
                return (float(eval(rule.amount_percentage_base, localdict)),
                        float(eval(rule.quantity, localdict)),
                        rule.amount_percentage)
            except:
                print(">>>>>>>>>>>>>> ", (float(eval(rule.amount_percentage_base, localdict)),
                        float(eval(rule.quantity, localdict)),
                        rule.amount_percentage))
                raise UserError(_('Wrong percentage base or quantity defined for salary rule %s (%s).') % (rule.name, rule.code))
        else:
            try:
                python_compute = rule.amount_python_compute
                print " python_compute >>>>>>>>>>>>> ", python_compute
                # python_compute = python_compute.replace('contract.', '')
                # print " python_compute >>>>>>>>>>>>> ", python_compute
                eval(python_compute, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), 'result_qty' in localdict and localdict['result_qty'] or 1.0, 'result_rate' in localdict and localdict['result_rate'] or 100.0
            except:
                print("??????????????? ", eval(python_compute, localdict, mode='exec', nocopy=True))
                raise UserError(_('Wrong python code defined for salary rule %s (%s).') % (rule.name, rule.code))


    @api.cr_uid_ids_context
    def _recursive_search_of_rules(self, cr, uid, rule_ids, context=None):
        """
        @param rule_ids: list of browse record
        @return: returns a list of tuple (id, sequence) which are all the children of the passed rule_ids
        """
        children_rules = []
        for rule in rule_ids:
            if rule.child_ids:
                children_rules += self._recursive_search_of_rules(cr, uid, rule.child_ids, context=context)
        return [(r.id, r.sequence) for r in rule_ids] + children_rules


    @api.cr_uid_ids_context
    def get_all_rules(self, cr, uid, structure_ids, context=None):
        """
        @param structure_ids: list of structure
        @return: returns a list of tuple (id, sequence) of rules that are maybe to apply
        """

        all_rules = []
        for struct in self.browse(cr, uid, structure_ids, context=context):
            all_rules += self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, struct.rule_ids, context=context)
        print ">>>>>>>>>>>>>all_rules ", all_rules
        return all_rules