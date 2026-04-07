# Copyright (c) 2026, osama.ahmed@deliverydevs.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LEAVEDECLARATION(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		company: DF.Link
		data: DF.Data
		designation: DF.Link | None
		employee: DF.Link
		employee_name: DF.Data | None
		leave_days: DF.Float
		leave_end_date: DF.Date | None
		leave_start_date: DF.Date
		leaving_date: DF.Date
		passport_number: DF.Data
	# end: auto-generated types
	pass
