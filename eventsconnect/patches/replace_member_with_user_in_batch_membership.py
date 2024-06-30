import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_batch_membership")
	memberships = frappe.get_all("Events Connect Enrollment", ["member", "name"])
	for membership in memberships:
		email = frappe.db.get_value("Community Member", membership.member, "email")
		frappe.db.set_value("Events Connect Enrollment", membership.name, "member", email)
