import frappe


def execute():
	assignment_lessons = frappe.get_all(
		"Event Lesson", {"file_type": ["is", "set"]}, ["name", "question"]
	)

	for lesson in assignment_lessons:
		if not lesson.question:
			frappe.db.set_value("Event Lesson", lesson.name, "file_type", "")
