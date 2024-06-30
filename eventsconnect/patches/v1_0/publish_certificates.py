import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_certificate")
	certificates = frappe.get_all("EventsConnect Certificate", pluck="name")

	for certificate in certificates:
		frappe.db.set_value("EventsConnect Certificate", certificate, "published", 1)
