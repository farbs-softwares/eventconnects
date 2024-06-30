import frappe


def execute():
	value = frappe.db.get_single_value("EventsConnect Settings", "portal_event_creation")
	if value == "Event Instructor Role":
		frappe.db.set_value(
			"EventsConnect Settings", None, "portal_event_creation", "Event Creator Role"
		)
