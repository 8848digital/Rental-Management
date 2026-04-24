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
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date"
        },

        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date"
        }
    ]
};