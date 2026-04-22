# Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class LeaveSettlement(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from rental_management.rental_management.doctype.gratuity_pay.gratuity_pay import GratuityPay
		from rental_management.rental_management.doctype.leave_pay.leave_pay import LeavePay
		from rental_management.rental_management.doctype.salary_due.salary_due import SalaryDue
		from rental_management.rental_management.doctype.ticket_allowance.ticket_allowance import TicketAllowance

		adjustments_if_any: DF.Currency
		amended_from: DF.Link | None
		company: DF.Link
		date_of_settlement: DF.Date
		department: DF.Link | None
		doj__re_joining_date: DF.Date | None
		employee: DF.Link
		employee_name: DF.Data | None
		gratuity_pay: DF.Table[GratuityPay]
		last_working_day: DF.Date | None
		leave_pay: DF.Table[LeavePay]
		monthly_salary: DF.Currency
		other_allowance: DF.Currency
		other_deduction: DF.Currency
		outstanding_advance: DF.Currency
		overtime_allowance: DF.Currency
		position: DF.Link | None
		posting_date: DF.Date | None
		remark: DF.LongText | None
		salary_due: DF.Table[SalaryDue]
		ticket_allowance: DF.Table[TicketAllowance]
		total_deductions: DF.Currency
		total_entitlements: DF.Currency
		total_service: DF.Data | None
		total_settlement_payable: DF.Currency
		traffic_fine: DF.Currency
		type_of_settlement: DF.Literal["", "Vacation Settlement", "Final Settlement", "Labour Court Settlement", "Internal Transfer Settlement"]
	# end: auto-generated types
	pass

@frappe.whitelist()
def get_ticket_allowance(employee, settlement_date):
    """
    Returns unpaid Ticket Allowance records for an employee where the
    settlement date falls within the allowance cycle.
    """

    if not employee or not settlement_date:
        return []

    
    settlement_date = getdate(settlement_date)

    # Fetch ticket allowance records that match the settlement date
    tickets = frappe.get_all(
        "Ticket Allowance Detail",
        filters={
            "parent": employee,                
            "parenttype": "Employee",
            "paid": 0,
            "manual_paid":0,                         
            "from_date": ["<=", settlement_date],  
            "to_date": [">=", settlement_date]     
        },
        fields=["from_date", "to_date", "amount"],
        order_by="from_date asc"
    )

    result = []

    # Format data to match the structure expected by the client script
    for t in tickets:
        result.append({
            "from": t.from_date,
            "to": t.to_date,
            "amount": t.amount
        })


    return result

def mark_ticket_paid(doc, method):
    """
    Mark related Ticket Allowance Detail records as paid
    when Leave Settlement is submitted.
    """

    if not doc.ticket_allowance:
        return

    for row in doc.ticket_allowance:

        frappe.db.sql("""
            UPDATE `tabTicket Allowance Detail`
            SET paid = 1, reference = %s
            WHERE
                parent = %s
                AND from_date = %s
        """, (doc.name, doc.employee, row.get("from")))