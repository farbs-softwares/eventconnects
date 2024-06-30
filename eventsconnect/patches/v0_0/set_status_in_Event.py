import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	events = frappe.get_all(
		"EventsConnect Event", {"status": ("is", "not set")}, ["name", "published"]
	)
	for event in events:
		status = "Approved" if event.published else "In Progress"
		frappe.db.set_value("EventsConnect Event", event.name, "status", status)
