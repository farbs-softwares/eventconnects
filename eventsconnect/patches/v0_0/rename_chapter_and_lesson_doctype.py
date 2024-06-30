import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "event_chapter")
	frappe.reload_doc("eventsconnect", "doctype", "event_lesson")
	frappe.reload_doc("eventsconnect", "doctype", "chapter_reference")
	frappe.reload_doc("eventsconnect", "doctype", "lesson_reference")
	frappe.reload_doc("eventsconnect", "doctype", "exercise")
	frappe.reload_doc("eventsconnect", "doctype", "exercise_submission")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_batch_membership")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event_progress")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz")

	if not frappe.db.count("Event Chapter"):
		move_chapters()

	if not frappe.db.count("Event Lesson"):
		move_lessons()

	change_parent_for_lesson_reference()


def move_chapters():
	docs = frappe.get_all("Chapter", fields=["*"])
	for doc in docs:
		if frappe.db.exists("EventsConnect Event", doc.event):
			name = doc.name
			doc.update({"doctype": "Event Chapter"})
			del doc["name"]
			new_doc = frappe.get_doc(doc)
			new_doc.save()
			frappe.rename_doc("Event Chapter", new_doc.name, name)


def move_lessons():
	docs = frappe.get_all("Lesson", fields=["*"])
	for doc in docs:
		if frappe.db.exists("Chapter", doc.chapter):
			name = doc.name
			doc.update({"doctype": "Event Lesson"})
			del doc["name"]
			new_doc = frappe.get_doc(doc)
			new_doc.save()
			frappe.rename_doc("Event Lesson", new_doc.name, name)


def change_parent_for_lesson_reference():
	lesson_reference = frappe.get_all("Lesson Reference", fields=["name", "parent"])
	for reference in lesson_reference:
		frappe.db.set_value(
			"Lesson Reference", reference.name, "parenttype", "Event Chapter"
		)
