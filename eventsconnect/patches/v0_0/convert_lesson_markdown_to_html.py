import frappe
from eventsconnect.eventsconnect.md import markdown_to_html


def execute():
	lessons = frappe.get_all("Event Lesson", fields=["name", "body"])

	for lesson in lessons:
		html = markdown_to_html(lesson.body)
		frappe.db.set_value("Event Lesson", lesson.name, "body", html)

	frappe.reload_doc("eventsconnect", "doctype", "event_lesson")
