import frappe
from frappe.model.rename_doc import rename_doc


def execute():
	if frappe.db.exists("DocType", "EventsConnect Enrollment"):
		return

	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "EventsConnect Batch Membership", "EventsConnect Enrollment")
	frappe.flags.ignore_route_conflict_validation = False

	frappe.reload_doctype("EventsConnect Enrollment", force=True)
