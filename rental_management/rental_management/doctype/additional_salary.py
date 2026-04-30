import frappe
import json
from frappe.utils import get_link_to_form

def validate_child(self):
    for row in self.custom_penalties_detail:

        if not row.employee_deduction_reference:
            continue

        # Fetch REAL remaining from Employee Deduction Detail
        remaining = frappe.db.get_value(
            "Employee Deduction Detail",
            row.employee_deduction_reference,
            "remaining_amount"
        )

        if remaining is None:
            frappe.throw(
                f"Invalid reference in row #{row.idx}: {row.employee_deduction_reference}"
            )

        #  VALIDATION
        if row.installation_amount > remaining:
            frappe.throw(
                f"""Row #{row.idx}:
                Installation Amount ({row.installation_amount})
                cannot be greater than Remaining Amount ({remaining})
                """
            )

def validate(self, method):
    validate_child(self)
    if self.salary_component == "Total Deduction":
        total = 0

        for row in self.custom_penalties_detail:
            total += row.installation_amount or 0

        self.amount = total

@frappe.whitelist()
def get_deduction_by_payroll_date(employee, payroll_date):

    data = frappe.db.sql("""
        SELECT 
            name,
            type_of_penalty,
            remaining_amount,
            deduction_date,
            installment_amount,
            remarks
        FROM `tabEmployee Deduction Detail`
        WHERE 
            parent IN (
                SELECT name FROM `tabEmployee Deduction`
                WHERE employee = %s AND docstatus = 1
            )
            AND payroll_start_date <= %s
            AND (
                payrol_end_date IS NULL OR payrol_end_date >= %s
            )
            AND status != 'Paid'
        ORDER BY deduction_date ASC
    """, (employee, payroll_date, payroll_date), as_dict=1)

    return {"rows": data}


@frappe.whitelist()
def get_deduction_by_date_range(employee, from_date, to_date):

    data = frappe.db.sql("""
        SELECT 
            name,
            type_of_penalty,
            remaining_amount,
            deduction_date,
            installment_amount,
            remarks
        FROM `tabEmployee Deduction Detail`
        WHERE 
            parent IN (
                SELECT name FROM `tabEmployee Deduction`
                WHERE employee = %s AND docstatus = 1
            )
            AND payroll_start_date <= %s
            AND (
                payrol_end_date IS NULL OR payrol_end_date >= %s
            )
            AND IFNULL(status, '') != 'Paid'
        ORDER BY deduction_date ASC
    """, (employee, to_date, from_date), as_dict=1)

    return {"rows": data}


def on_submit(self,method):
        # Apply deduction when salary is submitted
        update_deductions(self)

def on_cancel(self,method):
        # Reverse deduction when salary is cancelled
        reverse_deductions(self)



def update_deductions(doc):

    if not doc.employee:
        return

    for row in doc.custom_penalties_detail:

        if not row.employee_deduction_reference or not row.installation_amount:
            continue

        d = frappe.db.get_value(
            "Employee Deduction Detail",
            row.employee_deduction_reference,
            ["remaining_amount", "paid_amount", "parent", "reference"],
            as_dict=1
        )

        if not d:
            continue

        if row.installation_amount > d.remaining_amount:
            frappe.throw(f"Row {row.idx}: Amount exceeds remaining")

        deduct = row.installation_amount

        new_paid = (d.paid_amount or 0) + deduct
        new_remaining = d.remaining_amount - deduct

        status = "Paid" if new_remaining <= 0 else "Partial Paid"

        link = get_link_to_form("Additional Salary", doc.name)

        existing_ref = d.reference or ""
        refs = [r.strip() for r in existing_ref.split("<br>") if r.strip()]

        if link not in refs:
            refs.append(link)

        updated_reference = "<br>".join(refs)

        frappe.db.set_value(
            "Employee Deduction Detail",
            row.employee_deduction_reference,
            {
                "paid_amount": new_paid,
                "remaining_amount": new_remaining,
                "status": status,
                "reference": updated_reference
            }
        )

        update_parent_totals(d.parent)

def reverse_deductions(doc):

    if not doc.employee:
        return

    for row in doc.custom_penalties_detail:

        if not row.employee_deduction_reference or not row.installation_amount:
            continue

        d = frappe.db.get_value(
            "Employee Deduction Detail",
            row.employee_deduction_reference,
            ["remaining_amount", "paid_amount", "parent", "reference"],
            as_dict=1
        )

        if not d:
            continue

        reverse = row.installation_amount

        new_paid = max((d.paid_amount or 0) - reverse, 0)
        new_remaining = d.remaining_amount + reverse

        if new_paid == 0:
            status = "Unpaid"
        elif new_remaining == 0:
            status = "Paid"
        else:
            status = "Partial Paid"

        link = get_link_to_form("Additional Salary", doc.name)

        existing_ref = d.reference or ""
        refs = [r.strip() for r in existing_ref.split("<br>") if r.strip()]

        refs = [r for r in refs if r != link]

        updated_reference = "<br>".join(refs)

        frappe.db.set_value(
            "Employee Deduction Detail",
            row.employee_deduction_reference,
            {
                "paid_amount": new_paid,
                "remaining_amount": new_remaining,
                "status": status,
                "reference": updated_reference
            }
        )

        update_parent_totals(d.parent)
    
def update_parent_totals(parent):

    data = frappe.db.sql("""
        SELECT 
            SUM(deduction_amount) as total,
            SUM(paid_amount) as paid,
            SUM(remaining_amount) as remaining,
            COUNT(*) as total_rows,
            SUM(CASE WHEN status = 'Paid' THEN 1 ELSE 0 END) as paid_rows,
            SUM(CASE WHEN status = 'Unpaid' THEN 1 ELSE 0 END) as unpaid_rows
        FROM `tabEmployee Deduction Detail`
        WHERE parent = %s
    """, parent, as_dict=1)[0]

    total = data.total or 0
    paid = data.paid or 0
    remaining = data.remaining or 0

    total_rows = data.total_rows or 0
    paid_rows = data.paid_rows or 0
    unpaid_rows = data.unpaid_rows or 0

    if total_rows == 0:
        status = "Draft"
    elif paid_rows == total_rows:
        status = "Paid"
    elif unpaid_rows == total_rows:
        status = "Unpaid"
    else:
        status = "Partial Paid"

    frappe.db.set_value("Employee Deduction", parent, {
        "total_deduction": total,
        "paid_amount": paid,
        "remaining_balance": remaining,
        "status": status
    })