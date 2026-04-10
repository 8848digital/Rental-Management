import frappe
from frappe.utils import add_days, getdate, cint

def execute():
    employees = frappe.get_all(
        "Employee",
        fields=[
            "name",
            "final_confirmation_date",
            "custom_probation_period"
        ]
    )

    for emp in employees:
        if emp.final_confirmation_date and emp.custom_probation_period:
            probation_end_date = add_days(
                getdate(emp.final_confirmation_date),
                cint(emp.custom_probation_period)
            )

            frappe.db.set_value(
                "Employee",
                emp.name,
                "custom_probation_end_date",
                probation_end_date
            )

    frappe.db.commit()