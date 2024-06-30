import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_course_mentor_mapping")
	mappings = frappe.get_all("Events Connect Course Mentor Mapping", ["mentor", "name"])
	for mapping in mappings:
		email = frappe.db.get_value("Community Member", mapping.mentor, "email")
		frappe.db.set_value("Events Connect Course Mentor Mapping", mapping.name, "mentor", email)
