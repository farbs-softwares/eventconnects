import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course")
	frappe.reload_doc("eventsconnect", "doctype", "course_instructor")
	courses = frappe.get_all("Events Connect Course", fields=["name", "instructor"])
	for course in courses:
		doc = frappe.get_doc(
			{
				"doctype": "Course Instructor",
				"parent": course.name,
				"parentfield": "instructors",
				"parenttype": "Events Connect Course",
				"instructor": course.instructor,
			}
		)
		doc.save()
