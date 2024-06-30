import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	frappe.reload_doc("eventsconnect", "doctype", "chapter")
	frappe.reload_doc("eventsconnect", "doctype", "lesson")
	frappe.reload_doc("eventsconnect", "doctype", "lessons")
	frappe.reload_doc("eventsconnect", "doctype", "chapters")

	update_chapters()
	update_lessons()


def update_chapters():
	events = frappe.get_all("EventsConnect Event", pluck="name")
	for event in events:
		event_details = frappe.get_doc("EventsConnect Event", event)
		chapters = frappe.get_all("Chapter", {"event": event}, ["name"], order_by="index_")
		for chapter in chapters:
			event_details.append("chapters", {"chapter": chapter.name})

		event_details.save()


def update_lessons():
	chapters = frappe.get_all("Chapter", pluck="name")
	for chapter in chapters:
		chapter_details = frappe.get_doc("Chapter", chapter)
		lessons = frappe.get_all("Lesson", {"chapter": chapter}, ["name"], order_by="index_")
		for lesson in lessons:
			chapter_details.append("lessons", {"lesson": lesson.name})

		chapter_details.save()
