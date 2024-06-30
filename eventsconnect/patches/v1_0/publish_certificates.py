import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_certificate")
	certificates = frappe.get_all("Events Connect Certificate", pluck="name")

	for certificate in certificates:
		frappe.db.set_value("Events Connect Certificate", certificate, "published", 1)
