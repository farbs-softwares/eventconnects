import frappe


def execute():
	certificates = frappe.get_all("Events Connect Certificate", fields=["member", "name"])

	for certificate in certificates:
		if not frappe.db.exists(
			"DocShare",
			{
				"share_doctype": "Events Connect Certificate",
				"share_name": certificate.name,
				"user": certificate.member,
			},
		):
			share = frappe.get_doc(
				{
					"doctype": "DocShare",
					"user": certificate.member,
					"share_doctype": "Events Connect Certificate",
					"share_name": certificate.name,
					"read": 1,
				}
			)
			share.save(ignore_permissions=True)
