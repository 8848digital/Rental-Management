// Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Deduction Report"] = {
    "filters": [

        {
            "fieldname": "employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee"
        },

        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": "\nUnpaid\nPartial Paid\nPaid"
        },
        {
            "fieldname": "penalty_type",
            "label": "Penalty Type",
            "fieldtype": "Link",
            "options": "Penalties"
        },
        {
    fieldname: "deduction_date",
    label: "Deduction Date >=",
    fieldtype: "Date"
},
{
    fieldname: "payroll_start_date",
    label: "Payroll Start >=",
    fieldtype: "Date"
},
{
    fieldname: "salary_date",
    label: "Salary Payroll Date >=",
    fieldtype: "Date"
}
    ]
};