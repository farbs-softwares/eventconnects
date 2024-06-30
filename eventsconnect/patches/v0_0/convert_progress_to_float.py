import frappe
from frappe.utils import flt


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course_progress")
	progress_records = frappe.get_all("Events Connect Enrollment", fields=["name", "progress"])
	for progress in progress_records:
		frappe.db.set_value(
			"Events Connect Enrollment", progress.name, "progress", flt(progress.progress)
		)
