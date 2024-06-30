import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_quiz_submission")
	submissions = frappe.db.get_all("Events Connect Quiz Submission", fields=["name", "owner"])

	for submission in submissions:
		frappe.db.set_value(
			"Events Connect Quiz Submission", submission.name, "member", submission.owner
		)
