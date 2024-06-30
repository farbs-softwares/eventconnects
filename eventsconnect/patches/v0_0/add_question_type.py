import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_question")
	questions = frappe.get_all("Events Connect Quiz Question", pluck="name")

	for question in questions:
		frappe.db.set_value("Events Connect Quiz Question", question, "type", "Choices")
