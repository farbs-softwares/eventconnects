import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_batch_membership")
	memberships = frappe.get_all("EventsConnect Enrollment", ["member", "name"])
	for membership in memberships:
		email = frappe.db.get_value("Community Member", membership.member, "email")
		frappe.db.set_value("EventsConnect Enrollment", membership.name, "member", email)
