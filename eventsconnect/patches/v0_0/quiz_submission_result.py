import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_submission")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_result")
	results = frappe.get_all("EventsConnect Quiz Result", fields=["name", "result"])

	for result in results:
		value = 1 if result.result == "Right" else 0
		frappe.db.set_value("EventsConnect Quiz Result", result.name, "is_correct", value)
