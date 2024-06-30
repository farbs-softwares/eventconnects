import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event_mentor_mapping")
	mappings = frappe.get_all("EventsConnect Event Mentor Mapping", ["mentor", "name"])
	for mapping in mappings:
		email = frappe.db.get_value("Community Member", mapping.mentor, "email")
		frappe.db.set_value("EventsConnect Event Mentor Mapping", mapping.name, "mentor", email)
