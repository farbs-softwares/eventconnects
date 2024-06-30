import frappe


def execute():
	fields = [
		"courses",
		"batches",
		"certified_participants",
		"eventjobs",
		"statistics",
		"notifications",
	]

	for field in fields:
		frappe.db.set_single_value("EventsConnect Settings", field, 1)
