import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_certificate")
	default_certificate_template = frappe.db.get_value(
		"Property Setter",
		{
			"doc_type": "Events Connect Certificate",
			"property": "default_print_format",
		},
		"value",
	)

	if frappe.db.exists("Print Format", default_certificate_template):
		certificates = frappe.get_all("Events Connect Certificate", pluck="name")
		for certificate in certificates:
			frappe.db.set_value(
				"Events Connect Certificate", certificate, "template", default_certificate_template
			)
