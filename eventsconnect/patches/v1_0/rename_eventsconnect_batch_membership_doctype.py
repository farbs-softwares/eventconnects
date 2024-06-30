import frappe
from frappe.model.rename_doc import rename_doc


def execute():
	if frappe.db.exists("DocType", "Events Connect Enrollment"):
		return

	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Events Connect Batch Membership", "Events Connect Enrollment")
	frappe.flags.ignore_route_conflict_validation = False

	frappe.reload_doctype("Events Connect Enrollment", force=True)
