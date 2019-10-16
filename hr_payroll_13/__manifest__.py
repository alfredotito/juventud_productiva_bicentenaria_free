#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payroll v13',
    'category': 'Human Resources',
    'sequence': 1,
    "author" : "JUVENTUD PRODUCTIVA VENEZOLANA",
    'summary': 'Adaptation of the payroll module v12 for version 13 of odoo community',
    "website" : "https://www.youtube.com/channel/UCTj66IUz5M-QV15Mtbx_7yg",
    'license': 'AGPL-3',
    'description': "This module is an adaptation of the Payroll module from version 12 of odoo to 13.",
    'depends': [
        'hr_contract',
        'hr_holidays',
    ],
    'data': [
        'security/hr_payroll_security.xml',
        'security/ir.model.access.csv',
        'wizard/hr_payroll_payslips_by_employees_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_salary_rule_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_employee_views.xml',
        'data/hr_payroll_sequence.xml',
        'views/hr_payroll_report.xml',
        'data/hr_payroll_data.xml',
        'wizard/hr_payroll_contribution_register_report_views.xml',
        'views/report_contributionregister_templates.xml',
        'views/report_payslip_templates.xml',
        'views/report_payslipdetails_templates.xml',
    ],
    'demo': ['data/hr_payroll_demo.xml'],
    'images': ['static/images/payroll_screenshot.png'],
    "active": True,
    "installable": True,
}
