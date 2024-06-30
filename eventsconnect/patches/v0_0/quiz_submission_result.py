import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_submission")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_result")
	results = frappe.get_all("Events Connect Quiz Result", fields=["name", "result"])

	for result in results:
		value = 1 if result.result == "Right" else 0
		frappe.db.set_value("Events Connect Quiz Result", result.name, "is_correct", value)
