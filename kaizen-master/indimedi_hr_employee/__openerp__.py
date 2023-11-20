# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Indimedi Employee Check List',
    'version' : '1.1',
    'summary': "Allow to Employee's joining checklist and exit checklist.",
    'sequence': 14,
    'Author': "Indimedi Solutions Pvt. Ltd.",
    'description': """
Employee Check List
====================
In employee form, there will be three tabs Employee details, Joining Checklist, Kaizen Tenure, Exit Formalities

In employee details tab capture all the basic details related to employee.
    """,
    'category': 'HR Employee',
    'website': 'https://www.indimdi.in',
    'images' : [],
    'depends' : ['base', 'hr', 'hr_contract', 'indimedi_kra'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
        'views/hr_contract_view.xml',
        'data/employee_kaizen_data.xml',
        'data/employee_kaizen_document_demo.xml',
        'data/employee_exit_check_list_data.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
