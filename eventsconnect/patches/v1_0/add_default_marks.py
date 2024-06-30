import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_question")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz")
	questions = frappe.get_all("EventsConnect Quiz Question", pluck="name")

	for question in questions:
		frappe.db.set_value("EventsConnect Quiz Question", question, "marks", 1)

	quizzes = frappe.get_all("EventsConnect Quiz", pluck="name")

	for quiz in quizzes:
		questions_count = frappe.db.count("EventsConnect Quiz Question", {"parent": quiz})
		frappe.db.set_value(
			"EventsConnect Quiz", quiz, {"total_marks": questions_count, "passing_percentage": 100}
		)
