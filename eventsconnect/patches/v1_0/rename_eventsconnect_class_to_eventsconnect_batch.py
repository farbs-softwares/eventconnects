import frappe
from frappe.model.rename_doc import rename_doc


def execute():
	if frappe.db.exists("DocField", {"fieldname": "students", "parent": "EventsConnect Batch"}):
		return

	rename_eventsconnect_class()
	rename_class_student()
	rename_class_events()


def rename_eventsconnect_class():
	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "EventsConnect Class", "EventsConnect Batch")
	frappe.flags.ignore_route_conflict_validation = False
	frappe.reload_doctype("EventsConnect Batch", force=True)


def rename_class_student():
	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Class Student", "Batch Student")
	frappe.flags.ignore_route_conflict_validation = False
	frappe.reload_doctype("Batch Student", force=True)


def rename_class_events():
	frappe.flags.ignore_route_conflict_validation = True
	rename_doc("DocType", "Class Event", "Batch Event")
	frappe.flags.ignore_route_conflict_validation = False
	frappe.reload_doctype("Batch Event", force=True)
