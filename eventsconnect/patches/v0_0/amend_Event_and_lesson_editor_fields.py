import frappe
from frappe.utils import to_markdown


def execute():
	amend_lesson_content()
	amend_event_description()


def amend_lesson_content():
	lesson_content_field = frappe.db.get_value(
		"DocField", {"parent": "Event Lesson", "fieldname": "body"}, "fieldtype"
	)

	if lesson_content_field == "Text Editor":
		lessons = frappe.get_all("Event Lesson", fields=["name", "body"])

		for lesson in lessons:
			frappe.db.set_value("Event Lesson", lesson.name, "body", to_markdown(lesson.body))

		frappe.reload_doc("eventsconnect", "doctype", "event_lesson")


def amend_event_description():
	event_description_field = frappe.db.get_value(
		"DocField", {"parent": "EventsConnect Event", "fieldname": "description"}, "fieldtype"
	)

	if event_description_field == "Text Editor":
		events = frappe.get_all("EventsConnect Event", fields=["name", "description"])

		for event in events:
			frappe.db.set_value(
				"EventsConnect Event", event.name, "description", to_markdown(event.description)
			)

		frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
