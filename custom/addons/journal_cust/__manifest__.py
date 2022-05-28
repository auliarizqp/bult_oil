# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{

    "name": "account journal",
    "version": "15.0.0.0",
    
    "summary": "",
    "category": "Industries",
    "description": """
    BrowseInfo developed a new odoo/OpenERP module apps
    This module is used to manage Hospital and Healthcare Management and Clinic Management apps. 
    manage clinic manage Patient hospital in odoo manage Healthcare system Patient Management, 
    Odoo Hospital Management odoo Healthcare Management Odoo Clinic Management
    Odoo hospital Patients
    Odoo Healthcare Patients Card Report
    Odoo Healthcare Patients Medication History Report
    Odoo Healthcare Appointments
    Odoo hospital Appointments Invoice
    Odoo Healthcare Families Prescriptions Healthcare Prescriptions
    Odoo Healthcare Create Invoice from Prescriptions odoo hospital Prescription Report
    Odoo Healthcare Patient Hospitalization
    odoo Hospital Management System
    Odoo Healthcare Management System
    Odoo Clinic Management System
    Odoo Appointment Management System
    health care management system
    Generate Report for patient details, appointment, prescriptions, lab-test

    Odoo Lab Test Request and Result
    Odoo Patient Hospitalization details
    Generate Patient's Prescriptions

    
""",

    "depends": ["base"],
    "data": [
        'security/hospital_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/account-journal-report.xml',
        'views/account-journal.xml',
    ],
    "author": "BrowseInfo",
    "website": "https://www.browseinfo.in",
    "installable": True,
    "application": True,
    "auto_install": False,
    "license":'OPL-1',

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
