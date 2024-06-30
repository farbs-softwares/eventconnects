import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course")
	courses = frappe.get_all(
		"EventsConnect Course", {"status": ("is", "not set")}, ["name", "published"]
	)
	for course in courses:
		status = "Approved" if course.published else "In Progress"
		frappe.db.set_value("EventsConnect Course", course.name, "status", status)
