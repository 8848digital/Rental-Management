# Copyright (c) 2025, osama.ahmed@deliverydevs.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe.utils import today

class LOA(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from rental_management.rental_management.doctype.loa_locations_cdt.loa_locations_cdt import LOAlocationscdt

		active: DF.Check
		allocated_driver_quota: DF.Int
		allocated_vehicle_quota: DF.Int
		amended_from: DF.Link | None
		client: DF.Link
		contract_number: DF.Data | None
		contract_year: DF.Int
		document: DF.Attach | None
		end_user: DF.Link | None
		expiry_date: DF.Date
		issue_date: DF.Date
		issuing_authority: DF.Link
		license_expiry_date: DF.Date | None
		license_issue_date: DF.Date | None
		loa_number: DF.Data
		loa_status: DF.Literal["", "Active", "Expired", "Cancelled"]
		locations: DF.Table[LOAlocationscdt]
		mother_attachment: DF.Attach | None
		ref_no: DF.Data | None
		remaining_driver_quota: DF.Int
		remaining_vehicle_quota: DF.Int
		total_cancelled_driver_cicpa: DF.Int
		total_cancelled_vehicle_cicpa: DF.Int
		total_created_driver_cicpa: DF.Int
		total_created_vehicle_cicpa: DF.Int
		total_driver_quota: DF.Int
		total_vehicle_quota: DF.Int
	# end: auto-generated types
	
	def validate(self):
		self.set_loa_status()

	def on_cancel(self):
		self.db_set("loa_status", "Cancelled")

	def set_loa_status(self):

		if self.expiry_date and self.expiry_date < today():
			self.loa_status = "Expired"

		else:
			self.loa_status = "Active"


def update_expired_loa_status():

	expired_loas = frappe.get_all(
		"LOA",
		filters={
			"expiry_date": ["<", today()],
			"docstatus": ["!=", 2],
			"loa_status": ["!=", "Expired"]
		},
		pluck="name"
	)

	for loa in expired_loas:

		frappe.db.set_value(
			"LOA",
			loa,
			{
				"loa_status": "Expired"
			},
			update_modified=False
		)

	active_loas = frappe.get_all(
		"LOA",
		filters={
			"expiry_date": [">=", today()],
			"docstatus": ["!=", 2],
			"loa_status": ["!=", "Active"]
		},
		pluck="name"
	)

	for loa in active_loas:

		frappe.db.set_value(
			"LOA",
			loa,
			{
				"loa_status": "Active"
			},
			update_modified=False
		)
