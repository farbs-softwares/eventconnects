import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course")
	frappe.reload_doc("eventsconnect", "doctype", "course_instructor")
	courses = frappe.get_all("EventsConnect Course", fields=["name", "instructor"])
	for course in courses:
		doc = frappe.get_doc(
			{
				"doctype": "Course Instructor",
				"parent": course.name,
				"parentfield": "instructors",
				"parenttype": "EventsConnect Course",
				"instructor": course.instructor,
			}
		)
		doc.save()
