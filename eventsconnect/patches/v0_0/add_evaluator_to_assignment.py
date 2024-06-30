import frappe


def execute():
	if frappe.db.exists("DocType", "Lesson Assignment"):
		frappe.reload_doc("eventsconnect", "doctype", "lesson_assignment")
		assignments = frappe.get_all("Lesson Assignment", fields=["name", "course"])
		for assignment in assignments:
			evaluator = frappe.db.get_value("Events Connect Course", assignment.course, "evaluator")
			frappe.db.set_value("Lesson Assignment", assignment.name, "evaluator", evaluator)
