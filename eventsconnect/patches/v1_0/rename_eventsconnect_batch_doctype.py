import frappe
from frappe.model.rename_doc import rename_doc


def execute():
	if frappe.db.exists("DocType", "Events Connect Batch Old"):
		return

	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Events Connect Batch", "Events Connect Batch Old")
	frappe.flags.ignore_route_conflict_validation = False

	frappe.reload_doctype("Events Connect Batch Old", force=True)
