import frappe


def execute():
	if (
		frappe.db.count("EventsConnect Course")
		and frappe.db.count("Course Chapter")
		and frappe.db.count("Course Lesson")
		and frappe.db.count("EventsConnect Quiz")
	):
		frappe.db.set_value("EventsConnect Settings", None, "is_onboarding_complete", True)
