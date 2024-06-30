import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	events = frappe.get_all("EventsConnect Event", fields=["name", "owner"])
	for event in events:
		frappe.db.set_value("EventsConnect Event", event.name, "instructor", event.owner)
