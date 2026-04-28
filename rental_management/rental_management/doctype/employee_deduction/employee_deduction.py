# Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class EmployeeDeduction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from rental_management.rental_management.doctype.employee_deduction_detail.employee_deduction_detail import EmployeeDeductionDetail

		amended_from: DF.Link | None
		department: DF.Link | None
		employee: DF.Link | None
		employee_deduction_detail: DF.Table[EmployeeDeductionDetail]
		employee_name: DF.Data | None
		naming_series: DF.Literal[None]
		paid_amount: DF.Currency
		remaining_balance: DF.Currency
		remarks: DF.Text | None
		status: DF.Literal["", "Draft", "Unpaid", "Partial Paid", "Paid"]
		total_deduction: DF.Currency
		transaction_date: DF.Date | None
	# end: auto-generated types
	pass
	def on_cancel(self):
			invalid_refs = []

			for row in self.employee_deduction_detail:
				if row.reference:
					refs = re.findall(r'>([^<]+)<', row.reference)

					for ref in refs:
						# Check if Additional Salary exists and is submitted
						if frappe.db.get_value("Additional Salary", ref, "docstatus") == 1:
							invalid_refs.append(ref)

			if invalid_refs:
				frappe.throw(
					"Please cancel the following Additional Salary document(s) first:<br><b>"
					+ "<br>".join(set(invalid_refs)) +
					"</b>"
				)
	def validate(self):
		self.update_child_payment()
		# Always keep parent totals and child calculations in sync
		self.update_totals()
		
	def on_update_after_submit(self):
		self.update_child_payment()
		self.update_parent_totals()
		self.db_update()
		for row in self.employee_deduction_detail:
			row.db_update()

	def update_child_payment(self):

			for row in self.employee_deduction_detail:

				row.deduction_amount = row.deduction_amount or 0
				row.paid_amount = row.paid_amount or 0

				if row.paid and row.partial_paid:
					frappe.throw(f"Row {row.idx}: Cannot select both Paid and Partial Paid")
					
				# ---------------- FULL PAID ----------------
				if row.paid:

					row.paid_amount = row.deduction_amount
					row.remaining_amount = 0
					row.status = "Paid"

				# ---------------- PARTIAL PAID ----------------
				elif row.partial_paid:

					if not row.partial_paid_amount or row.partial_paid_amount <= 0:
						frappe.throw(f"Row {row.idx}: Enter partial paid amount")

					if row.partial_paid_amount > row.remaining_amount:
						frappe.throw(f"Row {row.idx}: Partial amount exceeds remaining")

					# ADD TO EXISTING PAID
					row.paid_amount = min(
						row.deduction_amount,
						(row.paid_amount or 0) + row.partial_paid_amount
					)

					row.remaining_amount = row.deduction_amount - row.paid_amount

					if row.remaining_amount == 0:
						row.status = "Paid"
					else:
						row.status = "Partial Paid"

				# ---------------- NORMAL ----------------
				else:

					row.remaining_amount = row.deduction_amount - row.paid_amount

					if row.paid_amount == 0:
						row.status = "Unpaid"
					elif row.remaining_amount == 0:
						row.status = "Paid"
					else:
						row.status = "Partial Paid"

				# Float fix
				if abs(row.remaining_amount) < 0.001:
					row.remaining_amount = 0

	def update_parent_totals(self):

		total = 0
		paid = 0
		remaining = 0

		total_rows = 0
		paid_rows = 0
		unpaid_rows = 0

		for row in self.employee_deduction_detail:


			total += row.deduction_amount or 0
			paid += row.paid_amount or 0
			remaining += row.remaining_amount or 0

			total_rows += 1

			if row.status == "Paid":
				paid_rows += 1
			elif row.status == "Unpaid":
				unpaid_rows += 1

		self.total_deduction = total
		self.paid_amount = paid
		self.remaining_balance = remaining

		# Parent status
		if total_rows == 0:
			self.status = "Draft"
		elif paid_rows == total_rows:
			self.status = "Paid"
		elif unpaid_rows == total_rows:
			self.status = "Unpaid"
		else:
			self.status = "Partial Paid"

	def update_totals(self):

			total = 0
			paid = 0
			remaining = 0

			total_rows = 0
			paid_rows = 0
			unpaid_rows = 0

			for row in self.employee_deduction_detail:

				row.deduction_amount = row.deduction_amount or 0
				row.paid_amount = row.paid_amount or 0
				row.installment = row.installment or 0

				# Remaining calculation
				row.remaining_amount = row.deduction_amount - row.paid_amount

				if row.installment and row.installment > 0:
					row.installment_amount = row.remaining_amount / row.installment
				else:
					row.installment_amount = row.remaining_amount

				if row.paid_amount == 0:
					row.status = "Unpaid"
					unpaid_rows += 1
				elif row.paid_amount < row.deduction_amount:
					row.status = "Partial Paid"
				else:
					row.status = "Paid"
					paid_rows += 1

				total_rows += 1

				# Totals
				total += row.deduction_amount
				paid += row.paid_amount
				remaining += row.remaining_amount

			# Parent totals
			self.total_deduction = total
			self.paid_amount = paid
			self.remaining_balance = remaining

			# ---------------- PARENT STATUS ----------------
			if total_rows == 0:
				self.status = "Draft"

			elif paid_rows == total_rows:
				self.status = "Paid"

			elif unpaid_rows == total_rows:
				self.status = "Unpaid"

			else:
				self.status = "Partial Paid"