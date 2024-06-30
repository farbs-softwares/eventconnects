import frappe


def execute():
	value = frappe.db.get_single_value("Events Connect Settings", "portal_course_creation")
	if value == "Course Instructor Role":
		frappe.db.set_value(
			"Events Connect Settings", None, "portal_course_creation", "Course Creator Role"
		)
