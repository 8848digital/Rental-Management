# Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


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
		date_of_settlement: DF.Date | None
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
