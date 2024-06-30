import frappe
from frappe.utils import to_markdown


def execute():
	amend_lesson_content()
	amend_course_description()


def amend_lesson_content():
	lesson_content_field = frappe.db.get_value(
		"DocField", {"parent": "Course Lesson", "fieldname": "body"}, "fieldtype"
	)

	if lesson_content_field == "Text Editor":
		lessons = frappe.get_all("Course Lesson", fields=["name", "body"])

		for lesson in lessons:
			frappe.db.set_value("Course Lesson", lesson.name, "body", to_markdown(lesson.body))

		frappe.reload_doc("eventsconnect", "doctype", "course_lesson")


def amend_course_description():
	course_description_field = frappe.db.get_value(
		"DocField", {"parent": "EventsConnect Course", "fieldname": "description"}, "fieldtype"
	)

	if course_description_field == "Text Editor":
		courses = frappe.get_all("EventsConnect Course", fields=["name", "description"])

		for course in courses:
			frappe.db.set_value(
				"EventsConnect Course", course.name, "description", to_markdown(course.description)
			)

		frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course")
