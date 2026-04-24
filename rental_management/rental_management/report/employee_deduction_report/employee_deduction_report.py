# Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
# For license information, please see license.txt

import frappe
import re


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    # for row in data:
    #     row["reference"] = format_reference(row.get("reference"))

    return columns, data


def get_columns():
    return [
        {"label": "Deduction Doc", "fieldname": "parent", "fieldtype": "Link", "options": "Employee Deduction", "width": 180},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Penalty Type", "fieldname": "type_of_penalty", "fieldtype": "Link", "options": "Penalties", "width": 150},
        {"label": "Deduction Date", "fieldname": "deduction_date", "fieldtype": "Date", "width": 120},
        {"label": "Payroll Start", "fieldname": "payroll_start_date", "fieldtype": "Date", "width": 120},
        {"label": "Payroll End", "fieldname": "payrol_end_date", "fieldtype": "Date", "width": 120},
        {"label": "Amount", "fieldname": "deduction_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Remaining", "fieldname": "remaining_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]


def get_data(filters):

    conditions = ""
    values = {}
    # Filter by penalty type
    if filters.get("penalty_type"):
        conditions += " AND edd.type_of_penalty = %(penalty_type)s"
        values["penalty_type"] = filters.get("penalty_type")
    # Filter by employee
    if filters.get("employee"):
        conditions += " AND ed.employee = %(employee)s"
        values["employee"] = filters.get("employee")

    # Filter by status
    if filters.get("status"):
        conditions += " AND edd.status = %(status)s"
        values["status"] = filters.get("status")

    # Date overlap filter (IMPORTANT FIX)
    if filters.get("from_date") and filters.get("to_date"):
        conditions += """
            AND edd.payroll_start_date <= %(to_date)s
            AND edd.payrol_end_date >= %(from_date)s
        """
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")

    data = frappe.db.sql(f"""
        SELECT
            edd.parent,
            ed.employee,
            ed.employee_name,
            edd.type_of_penalty,
            edd.deduction_date,
            edd.payroll_start_date,
            edd.payrol_end_date,
            edd.deduction_amount,
            edd.paid_amount,
            edd.remaining_amount,
            edd.status
        FROM `tabEmployee Deduction Detail` edd
        INNER JOIN `tabEmployee Deduction` ed
            ON ed.name = edd.parent
        WHERE 
            ed.docstatus = 1
            {conditions}
        ORDER BY ed.employee, edd.deduction_date ASC
    """, values, as_dict=1)

    return data