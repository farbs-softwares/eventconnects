import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_question")
	questions = frappe.get_all("EventsConnect Quiz Question", pluck="name")

	for question in questions:
		frappe.db.set_value("EventsConnect Quiz Question", question, "type", "Choices")
