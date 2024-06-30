import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_certification")
	certificates = frappe.get_all("EventsConnect Certification", fields=["name", "student"])
	for certificate in certificates:
		frappe.db.set_value(
			"EventsConnect Certification", certificate.name, "member", certificate.student
		)
