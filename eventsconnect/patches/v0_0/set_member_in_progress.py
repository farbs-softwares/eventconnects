import frappe


def execute():
	frappe.reload_doc("eventsconnect", "doctype", "eventsconnect_event_progress")
	progress_records = frappe.get_all(
		"EventsConnect Event Progress", fields=["name", "owner", "member"]
	)

	for progress in progress_records:
		if not progress.member:
			full_name = frappe.db.get_value("User", progress.owner, "full_name")
			frappe.db.set_value("EventsConnect Event Progress", progress.name, "member", progress.owner)
			frappe.db.set_value("EventsConnect Event Progress", progress.name, "member_name", full_name)
