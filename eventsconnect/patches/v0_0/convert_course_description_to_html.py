import frappe
from eventsconnect.eventsconnect.md import markdown_to_html


def execute():
	courses = frappe.get_all("EventsConnect Course", fields=["name", "description"])

	for course in courses:
		html = markdown_to_html(course.description)
		frappe.db.set_value("EventsConnect Course", course.name, "description", html)

	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course")
