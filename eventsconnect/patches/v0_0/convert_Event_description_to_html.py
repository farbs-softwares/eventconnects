import frappe
from eventsconnect.eventsconnect.md import markdown_to_html


def execute():
	events = frappe.get_all("EventsConnect Event", fields=["name", "description"])

	for event in events:
		html = markdown_to_html(event.description)
		frappe.db.set_value("EventsConnect Event", event.name, "description", html)

	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
