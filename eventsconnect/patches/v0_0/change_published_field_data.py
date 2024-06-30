import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	events = frappe.get_all("EventsConnect Event", fields=["name", "is_published"])
	for event in events:
		frappe.db.set_value("EventsConnect Event", event.name, "published", event.is_published)
