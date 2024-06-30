import frappe


def execute():
	if (
		frappe.db.count("Events Connect Course")
		and frappe.db.count("Course Chapter")
		and frappe.db.count("Course Lesson")
		and frappe.db.count("Events Connect Quiz")
	):
		frappe.db.set_value("Events Connect Settings", None, "is_onboarding_complete", True)
