import frappe
from frappe.utils import today, date_diff, add_days, flt

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def user_by_employee(doctype, txt, searchfield, start, page_len, filters):

    users = frappe.db.sql("""
        SELECT
            e.user_id as value,
            CONCAT(e.name, ' - ', e.employee_name) as description
        FROM
            `tabEmployee` e
        WHERE
            e.user_id IS NOT NULL
            AND e.user_id != ''
            AND e.status = 'Active'
            AND (e.name LIKE %(txt)s OR e.employee_name LIKE %(txt)s)
        LIMIT %(start)s, %(page_len)s
    """, {
        "txt": f"%{txt}%",
        "start": start,
        "page_len": page_len
    })

    return users

import frappe
from frappe.utils import today, date_diff, add_days, flt


def create_ticket_allowance():

    settings = frappe.get_single("Orion Settings")

    if not settings.ticket_entitlement_detail:
        return

    employees = frappe.get_all(
        "Employee",
        fields=["name", "designation", "date_of_joining"]
    )

    for emp in employees:

        if not emp.date_of_joining or not emp.designation:
            continue

        days_completed = date_diff(today(), emp.date_of_joining)

        for rule in settings.ticket_entitlement_detail:

            if not rule.designations:
                continue

            designation_list = [d.strip() for d in rule.designations.split(",")]

            if emp.designation not in designation_list:
                continue

            eligible_days = flt(rule.eligible_after_years_from_doj) * 365

            if days_completed < eligible_days:
                continue

            from_date = add_days(emp.date_of_joining, int(eligible_days))
            to_date = add_days(from_date, 365)

            exists = frappe.db.exists(
                "Ticket Allowance Detail",
                {
                    "parent": emp.name,
                    "parenttype": "Employee",
                    "from_date": from_date
                }
            )

            if exists:
                continue

            frappe.get_doc({
                "doctype": "Ticket Allowance Detail",
                "parent": emp.name,
                "parentfield": "custom_ticket_allowance_detail",
                "parenttype": "Employee",
                "from_date": from_date,
                "to_date": to_date,
                "amount": rule.amount,
                "paid": 0
            }).insert(ignore_permissions=True)

    frappe.db.commit()