import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "event_lesson")
	lessons = frappe.get_all("Event Lesson", fields=["name", "chapter"])
	for lesson in lessons:
		event = frappe.db.get_value("Event Chapter", lesson.chapter, "event")
		frappe.db.set_value("Event Lesson", lesson.name, "event", event)
