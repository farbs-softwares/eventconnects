import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_certification")
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_certificate")
	old = frappe.get_all(
		"EventsConnect Certification", fields=["name", "course", "student", "issue_date", "expiry_date"]
	)
	for data in old:
		frappe.get_doc(
			{
				"doctype": "EventsConnect Certificate",
				"course": data.course,
				"member": data.student,
				"issue_date": data.issue_date,
				"expiry_date": data.expiry_date,
			}
		).insert(ignore_permissions=True, ignore_mandatory=True)
