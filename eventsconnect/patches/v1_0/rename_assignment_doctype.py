import frappe
from frappe.model.rename_doc import rename_doc


def execute():
	if frappe.db.exists("DocType", "Events Connect Assignment Submission"):
		return

	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Lesson Assignment", "Events Connect Assignment Submission")
	frappe.flags.ignore_route_conflict_validation = False

	frappe.reload_doctype("Events Connect Assignment Submission", force=True)
