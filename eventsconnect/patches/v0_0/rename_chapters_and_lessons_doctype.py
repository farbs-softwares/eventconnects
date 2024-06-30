import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event")
	frappe.reload_doc("eventsconnect", "doctype", "chapter")
	frappe.reload_doc("eventsconnect", "doctype", "lesson")
	frappe.reload_doc("eventsconnect", "doctype", "chapter_reference")
	frappe.reload_doc("eventsconnect", "doctype", "lesson_reference")

	if not frappe.db.count("Chapter Reference"):
		move_chapters()

	if not frappe.db.count("Lesson Reference"):
		move_lessons()


def move_chapters():
	docs = frappe.get_all("Chapters", fields=["*"])
	for doc in docs:
		keys = doc
		keys.update({"doctype": "Chapter Reference"})
		del keys["name"]
		frappe.get_doc(keys).save()


def move_lessons():
	docs = frappe.get_all("Lessons", fields=["*"])
	for doc in docs:
		keys = doc
		keys.update({"doctype": "Lesson Reference"})
		del keys["name"]
		frappe.get_doc(keys).save()
