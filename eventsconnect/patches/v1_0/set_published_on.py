import frappe


def execute():
	courses = frappe.get_all(
		"Events Connect Course", filters={"published": 1}, fields=["name", "creation"]
	)

	for course in courses:
		frappe.db.set_value("Events Connect Course", course.name, "published_on", course.creation)
