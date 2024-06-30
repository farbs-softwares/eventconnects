import frappe
from frappe.model.rename_doc import rename_doc


def execute():
	if frappe.db.exists("DocType", "Events Connect Exercise"):
		return

	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Exercise", "Events Connect Exercise")
	frappe.flags.ignore_route_conflict_validation = False

	frappe.reload_doctype("Events Connect Exercise", force=True)
