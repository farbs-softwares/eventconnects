import frappe


def execute():
	if (
		frappe.db.count("EventsConnect Event")
		and frappe.db.count("Event Chapter")
		and frappe.db.count("Event Lesson")
		and frappe.db.count("EventsConnect Quiz")
	):
		frappe.db.set_value("EventsConnect Settings", None, "is_onboarding_complete", True)
