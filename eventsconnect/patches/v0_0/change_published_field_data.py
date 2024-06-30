import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course")
	courses = frappe.get_all("Events Connect Course", fields=["name", "is_published"])
	for course in courses:
		frappe.db.set_value("Events Connect Course", course.name, "published", course.is_published)
