import frappe


def execute():
	events = frappe.get_all(
		"EventsConnect Event", filters={"published": 1}, fields=["name", "creation"]
	)

	for event in events:
		frappe.db.set_value("EventsConnect Event", event.name, "published_on", event.creation)
