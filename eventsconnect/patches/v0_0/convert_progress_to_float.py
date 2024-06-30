import frappe
from frappe.utils import flt


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event_progress")
	progress_records = frappe.get_all("EventsConnect Enrollment", fields=["name", "progress"])
	for progress in progress_records:
		frappe.db.set_value(
			"EventsConnect Enrollment", progress.name, "progress", flt(progress.progress)
		)
